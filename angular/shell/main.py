"""模板应用入口（无边框窗口版）：窗口外观交给 axon-shell，界面仍由 web/ 决定。

    python main.py              # 用 web/dist
    WEB_ENV=dev python main.py  # 用 Vite 开发服务器 (127.0.0.1:5173)

跟默认模板的差别只有一行：AxonGUI -> AxonShellWindow。
"""

from __future__ import annotations

import http.server
import os
import socketserver
import sys
import threading
from pathlib import Path

from PySide6.QtWidgets import QApplication

from axon import AxonMagicGUI
from axon_shell import AxonShellWindow

import controller  # noqa: F401

BASE_DIR = Path(__file__).resolve().parent
WEB_NAME = "TemplateView"
ICON_FILE = BASE_DIR / "assets" / "icon-256.png"
DEV_URL = "http://127.0.0.1:5173/"


def _axon_shell_assets() -> Path | None:
    try:
        from axon_shell import assets_dir
    except Exception:  # noqa: BLE001
        return None
    return Path(assets_dir()).resolve()


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        sys.stderr.write("[axon] %s\n" % (fmt % args))

    def translate_path(self, path: str) -> str:
        if path.startswith("/axon-shell/"):
            assets = _axon_shell_assets()
            if assets is not None:
                name = path[len("/axon-shell/") :].split("?", 1)[0].split("#", 1)[0]
                candidate = (assets / name).resolve()
                if candidate.is_file() and assets in candidate.parents:
                    return str(candidate)
        return super().translate_path(path)


def start_server(directory: Path, port: int = 0, host: str = "127.0.0.1"):
    handler = __import__("functools").partial(_QuietHandler, directory=str(directory))
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer((host, port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def build_url() -> str:
    if os.environ.get("WEB_ENV") == "dev":
        return DEV_URL
    dist_dir = BASE_DIR / "web" / "dist" / "browser"
    if not (dist_dir / "index.html").is_file():
        print(f"[axon] 找不到前端构建产物: {dist_dir}", file=sys.stderr)
        print("[axon] 先执行: cd web && npm install && npm run build", file=sys.stderr)
        raise SystemExit(1)
    httpd = start_server(dist_dir)
    return f"http://127.0.0.1:{httpd.server_address[1]}/"


def main() -> int:
    if port := os.environ.get("AXON_DEBUGGER_PORT"):
        os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = f"127.0.0.1:{port}"

    url = build_url()
    app = QApplication(sys.argv[:1])
    AxonMagicGUI()
    view = AxonShellWindow(WEB_NAME, url, title="Axon Template", size=(1200, 742))
    try:
        from PySide6.QtGui import QIcon

        view.setWindowIcon(QIcon(str(ICON_FILE)))
    except Exception:  # noqa: BLE001
        pass
    view.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
