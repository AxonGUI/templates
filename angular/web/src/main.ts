import * as AxonLib from "axon-gui";
import { AxonInit } from "axon-gui";
import { bootstrapApplication } from "@angular/platform-browser";
import { appConfig } from "./app/app.config";
import { App } from "./app/app";

// 先连后端（在 AxonGUI 里 connected=true，普通浏览器里 connected=false），再渲染界面。
void (async () => {
  const status = await AxonInit();
  if (!status.ready) {
    console.warn("[axon] 没有连上 Python 后端:", status.reason ?? status.error);
  }

  // 无边框窗口版（axon-gui init --shell）：顶栏在 index.html 里，这里只负责启用拖拽。
  if (document.body.dataset["shell"] === "1") {
    const shell = (window as unknown as { AxonShell?: { init(o: unknown): void } }).AxonShell;
    shell?.init({ axon: AxonLib });
  }

  await bootstrapApplication(App, appConfig).catch((err) => console.error(err));
})();
