/**
 * 由 `axon-gui types` 生成，请勿手改。
 * axon-gui 5.4.7 · schema v1
 * 来源: controller
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
