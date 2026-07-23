#!/usr/bin/env python3
"""
Day 13 示例：重试装饰器 —— 企业级 API 调用的弹性保障

网络抖动、限流 429、服务端 5xx 时，自动重试是生产代码标配。
本模块用装饰器实现可配置的重试逻辑，Day 12 的 API 调用可直接套用。
"""
from __future__ import annotations

import functools
import random
import time
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    jitter: bool = True,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    重试装饰器工厂。

    Args:
        max_attempts: 最大尝试次数（含首次）
        delay: 首次重试前等待秒数
        backoff: 指数退避倍数，第 n 次等待 delay * backoff^(n-1)
        jitter: 是否加随机抖动，避免惊群效应
        exceptions: 触发重试的异常类型元组

    Example:
        @retry(max_attempts=3, exceptions=(requests.HTTPError, requests.Timeout))
        def call_api():
            ...
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)  # 保留原函数元信息 __name__, __doc__
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: Exception | None = None
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt == max_attempts:
                        break
                    # 计算等待时间
                    wait = current_delay
                    if jitter:
                        wait *= 0.5 + random.random()  # 0.5x ~ 1.5x
                    print(
                        f"[retry] {func.__name__} 第 {attempt} 次失败: {e}，"
                        f"{wait:.1f}s 后重试..."
                    )
                    time.sleep(wait)
                    current_delay *= backoff

            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator


# ---------- 演示：模拟不稳定的 API ----------
class RateLimitError(Exception):
    """模拟 429 限流。"""


_call_count = 0


@retry(max_attempts=4, delay=0.5, exceptions=(RateLimitError,))
def unstable_api_call(query: str) -> str:
    """
    模拟前两次调用失败、第三次成功的 API。
    被 @retry 装饰后，调用方无感知重试。
    """
    global _call_count
    _call_count += 1
    print(f"  -> unstable_api_call 第 {_call_count} 次执行, query={query!r}")
    if _call_count < 3:
        raise RateLimitError(f"模拟限流，当前第 {_call_count} 次")
    return f"成功响应: {query}"


def demo_retry() -> None:
    global _call_count
    _call_count = 0
    print("=== 重试装饰器演示 ===")
    result = unstable_api_call("NexusAgent")
    print(f"最终结果: {result}")
    print(f"总调用次数: {_call_count}")


if __name__ == "__main__":
    demo_retry()
