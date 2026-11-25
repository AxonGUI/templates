# Axon project template

This is the project skeleton that `axon-gui init <name>` copies. It contains a Python entry point
(`main.py`), an example controller (`controller/JSCallPY.py`) and a Vue 3 + Vite frontend
(`web/web-vue`).

```bash
# from the repository (or after `uv tool install axon-gui`)
python -m axon.cli init myapp     # or: axon-gui init myapp
cd myapp
uv sync
cd web/web-vue && npm install && npm run build && cd ../..
python main.py
```

`WEB_ENV=dev` points the window at the Vite dev server (`http://127.0.0.1:5173/`) instead of the
built `dist/`, so you get hot reload while working on the frontend.

---

## 中文

这是 `axon-gui init <name>` 拷贝出来的项目骨架：Python 入口 `main.py`、示例控制器
`controller/JSCallPY.py`、Vue 3 + Vite 前端 `web/web-vue`。

```bash
# 在本仓库里（或装好 axon-gui 之后）
python -m axon.cli init myapp     # 或 axon-gui init myapp
cd myapp
uv sync
cd web/web-vue && npm install && npm run build && cd ../..
python main.py
```

`WEB_ENV=dev` 时窗口加载 Vite dev server（`http://127.0.0.1:5173/`）而不是构建产物，改前端有热更新。
