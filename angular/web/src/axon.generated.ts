/**
 * 由 `axon-gui types` 生成，请勿手改。
 * axon-gui 5.5.0 · schema v1
 */

export interface AxonRegistry {
  /** 窗口: TemplateView */
  Greeter: {
    add(a?: number, b?: number): Promise<number>;
    greet(name?: string): Promise<string>;
  };
}

declare module "axon-gui" {
  interface AxonControllers extends AxonRegistry {}
}
