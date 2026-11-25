# Axon templates

Application templates for `axon-gui init` — one directory per frontend framework.

```bash
axon-gui init --list
axon-gui init myapp -t vue            # default
axon-gui init myapp -t react --shell  # frameless window (axon-shell)
```

| id | frontend | build output | entry HTML | `--shell` |
| --- | --- | --- | --- | --- |
| `vue` | Vue 3 + Vite + TS | `dist` | `web/index.html` | ✓ |
| `react` | React 19 + Vite + TS | `dist` | `web/index.html` | ✓ |
| `angular` | Angular 20 | `dist/browser` | `web/src/index.html` | ✓ |

`--shell` only swaps the entry pair (`shell/main.py`, `shell/index.html`) and rebuilds; frontend code stays untouched.

## Contract

`template.json` per template: `web.{dir,install,build,dist,index,dev}` and `shell.{main,index,deps}`.
`web.index` is the entry HTML relative to `web.dir` (Angular: `src/index.html`) — that is where `--shell` writes the title bar markup.

## Verify

```bash
python tools/verify_template.py --template react --shell
```

Copies the template into a temp dir, builds it, opens a real window, clicks the page button and asserts the Python round-trip (`你好，Axon！这句来自 Python。`).
