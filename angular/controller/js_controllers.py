"""由 `axon-gui types --js` 生成，请勿手改。

用法:

    from controller.js_controllers import connect

    api = connect("MainView")
    api.DocsJS.mirror({"hello": "world"})
"""

from __future__ import annotations

from typing import Any, Protocol, cast

# 没有在前端源码里找到 AxonController.register(...)
class AxonJsApi(Protocol):
    """所有已注册的前端控制器（跨窗口时是并集）。"""
    ...

def connect(web_name: str = "*") -> AxonJsApi:
    """拿到带类型的前端控制器入口。运行时就是 ``Axon(web_name)``。"""
    from axon import Axon

    return cast(AxonJsApi, Axon(web_name))
