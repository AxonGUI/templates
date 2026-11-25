import "axon-gui";

// 让 TypeScript 认识你的 Python 控制器：类名 -> 方法名。
declare module "axon-gui" {
  interface AxonPYController {
    Greeter: {
      greet(name?: string): Promise<string>;
      add(a?: number, b?: number): Promise<number>;
    };
  }
}
