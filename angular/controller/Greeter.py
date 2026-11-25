from axon import AxonController


@AxonController("TemplateView")
class Greeter:
    """JS 调用的控制器：AxonController 的第一个参数是「窗口名」，不是控制器名。

    控制器名默认就是类名（Greeter），所以页面里写 Axon.Greeter.greet("Axon")。
    想改名就传 id="OtherName"。
    """

    def greet(self, name: str = "world") -> str:
        return f"你好，{name}！这句来自 Python。"

    def add(self, a: int = 0, b: int = 0) -> int:
        return int(a) + int(b)
