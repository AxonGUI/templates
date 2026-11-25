"""契约测试：把一个模板真的跑起来，断言「页面 → Python → 页面」这条链通。

    python tools/verify_template.py --template vue
    python tools/verify_template.py --template angular --shell

前提：该模板的 web 依赖已安装、前端已构建（web/<dist> 里有 index.html）。
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECT_PY = "你好，Axon！这句来自 Python。"


def _manifest() -> dict:
    return json.loads((ROOT / "templates.json").read_text())


def _entry(tid: str) -> dict:
    for item in _manifest()["templates"]:
        if item["id"] == tid:
            return item
    raise SystemExit(f"没有这个模板: {tid}")


def _prepare(tpl_dir: Path, shell: bool) -> None:
    meta = json.loads((tpl_dir / "template.json").read_text())
    dist = tpl_dir / meta["web"]["dir"] / meta["web"]["dist"]
    if not (dist / "index.html").is_file():
        raise SystemExit(f"前端还没构建: {dist}")
    if shell:
        # 模拟 CLI 的 --shell：换成无边框入口 + 顶栏 HTML
        (tpl_dir / "main.py").write_text((tpl_dir / meta["shell"]["main"]).read_text())
        shell_html = (tpl_dir / meta["shell"]["index"]).read_text()
        # 各框架的入口 HTML 不一定在 web/index.html（Angular 在 web/src/index.html）
        web_index = meta["web"].get("index", "index.html")
        (tpl_dir / meta["web"]["dir"] / web_index).write_text(shell_html)
        # 和真实流程一致：先 --shell 换掉 index.html，再构建（dist 里才有那行 script）
        subprocess.run(meta["web"]["build"], cwd=tpl_dir / meta["web"]["dir"], shell=True, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--shell", action="store_true")
    args = ap.parse_args()

    entry = _entry(args.template)
    src_dir = ROOT / entry["dir"]
    meta0 = json.loads((src_dir / "template.json").read_text())
    web0 = src_dir / meta0["web"]["dir"]
    # 在临时目录里跑，别改坏仓库里的模板（--shell 会替换 main.py / index.html）
    work = Path(tempfile.mkdtemp(prefix=f"axverify-{args.template}-"))
    tpl_dir = work / "tpl"
    shutil.copytree(src_dir, tpl_dir, ignore=shutil.ignore_patterns("node_modules", "__pycache__", ".venv"))
    os.symlink(web0 / "node_modules", tpl_dir / meta0["web"]["dir"] / "node_modules")
    _prepare(tpl_dir, args.shell)

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault(
        "QTWEBENGINE_CHROMIUM_FLAGS", "--no-sandbox --disable-gpu --disable-dev-shm-usage"
    )
    sys.path.insert(0, str(tpl_dir))

    from PySide6.QtCore import Qt, QTimer  # noqa: PLC0415
    from PySide6.QtWidgets import QApplication  # noqa: PLC0415
    from axon import Axon, AxonGUI, AxonMagicGUI  # noqa: PLC0415

    app = QApplication(sys.argv[:1])
    AxonMagicGUI()
    mod = importlib.import_module("main")
    if args.shell:
        from axon_shell import AxonShellWindow  # noqa: PLC0415

        view = AxonShellWindow(mod.WEB_NAME, mod.build_url(), title="verify", size=(1000, 720))
    else:
        view = AxonGUI(mod.WEB_NAME, mod.build_url())
    def on_console(msg) -> None:
        text = msg.toString()
        if "error" in text.lower() or "axon" in text.lower():
            print(f"[page] {text}")

    view.page().javaScriptConsoleMessage = None  # type: ignore[assignment]
    try:
        view.page().javaScriptConsoleMessage = lambda level, text, line, src: print(f"[page] {text}")
    except Exception:  # noqa: BLE001
        pass
    view.show()

    state: dict = {"ok": False, "errors": []}

    def run_js(code: str, cb) -> None:
        view.page().runJavaScript(code, 0, cb)

    def fail(msg: str) -> None:
        state["errors"].append(msg)
        print(f"[verify] FAIL: {msg}")
        app.exit(1)

    def ask(code: str, timeout: float = 15.0):
        """同步跑一小段 JS（轮询事件循环，别在主线程里死等 future）。"""
        box: dict = {}
        run_js(code, lambda v: box.setdefault("v", v))
        end = time.monotonic() + timeout
        while "v" not in box and time.monotonic() < end:
            app.processEvents()
            time.sleep(0.02)
        return box.get("v")

    def step_click() -> None:
        run_js(
            "(document.querySelector('.btn') || document.querySelector('main button')).click(); 'ok'",
            lambda _v: QTimer.singleShot(300, step_wait_out),
        )

    def step_wait_out(deadline: float | None = None) -> None:
        deadline = deadline or (time.monotonic() + 20)
        text = ask("(document.querySelector('pre.out')||{}).textContent || ''", timeout=3)
        if text and "你好" in str(text):
            step_shell()
            return
        if time.monotonic() > deadline:
            return fail(f"点按钮后页面没有显示 Python 的返回（当前: {text!r}）")
        QTimer.singleShot(300, step_wait_out)

    def step_shell() -> None:
        if not args.shell:
            return finish()
        flags = bool(view.windowFlags() & Qt.WindowType.FramelessWindowHint)
        has = ask("typeof window.AxonShell === 'object'", timeout=3)
        regions = ask("JSON.stringify(window.AxonShell ? window.AxonShell.drag.regions() : [])", timeout=3)
        if not flags:
            return fail("--shell 模式下窗口应该没有系统边框")
        if not has:
            return fail("页面没有加载 /axon-shell/shell.js")
        try:
            count = len(json.loads(regions or "[]"))
        except json.JSONDecodeError:
            count = 0
        if count < 1:
            return fail(f"没有上报拖拽区（regions={regions!r}）")
        print(f"[verify] shell: frameless=True dragRegions={count}")
        finish()

    def finish() -> None:
        # 走到这里说明「点按钮 → Python 返回 → 页面显示」这条链已经通了。
        state["ok"] = True
        print(f"[verify] PASS template={args.template} shell={args.shell}")
        app.exit(0)

    def on_loaded(ok: bool) -> None:
        # 页面加载完再等一会儿：前端要跑 AxonInit() 连通道。
        if not ok:
            return fail("页面加载失败")
        QTimer.singleShot(1200, step_click)

    view.loadFinished.connect(on_loaded)
    QTimer.singleShot(120_000, lambda: (print("[verify] TIMEOUT"), app.exit(2)))
    rc = app.exec()
    view.close()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
