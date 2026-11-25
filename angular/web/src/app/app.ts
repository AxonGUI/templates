import { Component, signal } from "@angular/core";
import { Axon } from "axon-gui";

@Component({
  selector: "app-root",
  imports: [],
  templateUrl: "./app.html",
  styleUrl: "./app.css",
})
export class App {
  protected readonly info = signal("");

  protected async callPython(): Promise<void> {
    // JS → Python：函数名就是 Python 里的方法名，参数直接摊开传。
    this.info.set(String(await Axon.Greeter.greet("Axon")));
  }
}
