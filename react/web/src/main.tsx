import * as AxonLib from "axon-gui";
import { AxonInit } from "axon-gui";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./style.css";

// 先把界面挂上去：连不上后端也要能看到页面，不能白屏。
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

// 再探测通道：在 AxonGUI 里 connected=true，普通浏览器里 connected=false。
void AxonInit()
  .then((status) => {
    if (!status.ready) {
      console.warn("[axon] 没有连上 Python 后端:", status.reason ?? status.error);
      return;
    }
    // 无边框窗口版（axon-gui init --shell）：顶栏在 index.html 里，这里只负责启用拖拽。
    if (document.body.dataset.shell === "1") {
      const shell = (window as unknown as { AxonShell?: { init(o: unknown): void } }).AxonShell;
      shell?.init({ axon: AxonLib });
    }
  })
  .catch((err) => console.warn("[axon] AxonInit 失败:", err));
