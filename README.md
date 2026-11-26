# Axon 模板

`axon-gui init` 用的应用模板，一个目录一套前端框架。

```bash
axon-gui init --list                      # 列出模板
axon-gui init myapp -t vue                # 默认 Vue 3
axon-gui init myapp -t react              # React 19
axon-gui init myapp -t angular            # Angular 20
axon-gui init myapp -t react --shell      # 无边框窗口版（加 axon-shell）
```

模板不随框架发版，`axon-gui init` 每次都从本仓库 `main` 分支取最新版。

## 三套模板

| id | 前端 | 构建 | 入口 HTML | `--shell` |
| --- | --- | --- | --- | --- |
| `vue` | Vue 3 + Vite + TS | `npm run build` → `dist` | `web/index.html` | ✓ |
| `react` | React 19 + Vite + TS | `npm run build` → `dist` | `web/index.html` | ✓ |
| `angular` | Angular 20 | `npm run build` → `dist/browser` | `web/src/index.html` | ✓ |

`--shell` 就是把 `shell/main.py` 覆盖成入口、`shell/index.html` 覆盖成页面入口（顶栏 + 三个窗口按钮），再正常构建一次；前端代码不用改。

## 类型补全

每套模板都带两个脚本：

```bash
npm run types        # 重新生成 web/src/axon.generated.ts
npm run types:check  # 只校验（CI 用，生成物过期会失败）
```

Vue / React 模板还接了 `axon-gui/vite-plugin`：`npm run dev` 启动时和保存文件时自动重生成。
Angular 没有 Vite，改完 Python 控制器后手动跑一次 `npm run types`。

生成物长这样（举例）：

```ts
export interface AxonRegistry {
  Greeter: {
    add(a?: number, b?: number): Promise<number>;
    greet(name?: string): Promise<string>;
  };
}
declare module "axon-gui" {
  interface AxonControllers extends AxonRegistry {}
}
```

有了它，写前端时 `Axon.Greeter.greet(` 会有参数名与类型；写错参数、调用不存在的方法会直接报编译错误。

## 接入契约

`templates.json`（仓库根）只有一个索引：`{id, title, dir, description}`。

每个模板目录里的 `template.json` 是它跟 CLI 的契约：

```json
{
  "id": "vue",
  "title": "Vue 3 + Vite + TypeScript",
  "description": "……",
  "web": {
    "dir": "web",              // 前端工程目录
    "install": "npm install",  // 装依赖
    "build": "npm run build",  // 构建
    "dist": "dist",            // 构建产物目录（相对 web.dir，Angular 是 dist/browser）
    "index": "index.html",     // 入口 HTML（相对 web.dir，Angular 是 src/index.html）
    "dev": "npm run dev"       // 开发服务器
  },
  "shell": {
    "main": "shell/main.py",   // 无边框窗口入口
    "index": "shell/index.html", // 替换入口 HTML
    "deps": ["axon-shell>=0.2.2"] // --shell 时额外写进 pyproject 的依赖
  }
}
```

另外三条约定：

1. `main.py` 从 `web/<dist>` 起静态服务，页面地址用 `AxonGUI(WEB_NAME, url)` 或 `AxonShellWindow(...)`。
2. 页面里先挂载界面、再 `await AxonInit()`（别让通道初始化挡住首屏）。
3. 控制器放在 `controller/`，`@AxonController("TemplateView")` 的窗口名要和 `main.py` 里的 `WEB_NAME` 一致。

## 加一套新模板

1. 新建目录，把前端工程放 `web/`；
2. 写 `template.json`（字段同上），往 `templates.json` 里加一行索引；
3. 写 `main.py`、`controller/Greeter.py`（`greet(name)` 返回带 Python 痕迹的一句话）；
4. 加 `shell/main.py` + `shell/index.html`（顶栏用 `data-axon-drag`，按钮用 `data-axon-window="min|max|close"`）；
5. `python tools/verify_template.py --template <id>`（加 `--shell` 再跑一次）。

## 验证

```bash
python tools/verify_template.py --template vue
python tools/verify_template.py --template react --shell
python tools/verify_template.py --template angular --shell
```

它在临时目录里复制模板、构建、开真窗口、点页面按钮，断言页面显示 `你好，Axon！这句来自 Python。`；`--shell` 还会断言无边框、`window.AxonShell` 存在、拖拽区非空。
