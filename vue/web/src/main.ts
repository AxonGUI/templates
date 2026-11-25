import * as AxonLib from "axon-gui";
import { AxonInit } from "axon-gui";
import { createApp } from "vue";
import App from "./App.vue";
import "./style.css";

// AxonInit() 会先探测通道: 在 AxonGUI 里返回 { connected: true },
// 直接拿浏览器打开则返回 { connected: false } —— 此时页面依然可以正常渲染。
const status = await AxonInit();
if (!status.ready) {
  console.warn("[axon] 没有连上 Python 后端:", status.reason ?? status.error);
}

// 无边框窗口版（axon-gui init --shell）：顶栏在 index.html 里，这里只负责启用拖拽。
if (document.body.dataset.shell === "1") {
  const shell = (window as unknown as { AxonShell?: { init(o: unknown): void } }).AxonShell;
  shell?.init({ axon: AxonLib });
}

createApp(App).mount("#app");
