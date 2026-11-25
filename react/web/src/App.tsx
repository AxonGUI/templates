import { useState } from "react";
import { Axon } from "axon-gui";

export default function App() {
  const [info, setInfo] = useState<string>("");

  async function callPython() {
    // JS → Python：函数名就是 Python 里的方法名，参数直接摊开传。
    setInfo(String(await Axon.Greeter.greet("Axon")));
  }

  return (
    <main className="app">
      <h1>Axon + React</h1>
      <p className="hint">点下面的按钮，会真的调用 Python 里的 Greeter.greet()。</p>
      <button type="button" className="btn" onClick={callPython}>
        调一次 Python
      </button>
      <pre className="out">{info || "还没有调用"}</pre>
    </main>
  );
}
