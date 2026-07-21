#!/usr/bin/env python3
"""
Day 13 示例：asyncio 异步编程入门

FastAPI（Day 15+）基于 async/await。今日掌握协程、并发调用多个 API 的基础。
"""
from __future__ import annotations

import asyncio
import time
from typing import Any


async def fetch_data(source: str, delay: float) -> dict[str, Any]:
    """
    模拟异步 IO：等待 delay 秒后返回数据。
    await 会挂起当前协程，让事件循环执行其他任务。
    """
    print(f"[{source}] 开始请求...")
    await asyncio.sleep(delay)  # 非阻塞等待，模拟网络 IO
    print(f"[{source}] 完成 ({delay}s)")
    return {"source": source, "data": f"{source} 的响应内容"}


async def fetch_sequential() -> list[dict]:
    """串行调用：总耗时 = 各 delay 之和。"""
    print("\n--- 串行调用 ---")
    t0 = time.perf_counter()
    results = []
    for name, delay in [("OpenAI", 1.0), ("Qwen", 1.0), ("DeepSeek", 1.0)]:
        results.append(await fetch_data(name, delay))
    elapsed = time.perf_counter() - t0
    print(f"串行总耗时: {elapsed:.2f}s")
    return results


async def fetch_parallel() -> list[dict]:
    """并行调用：asyncio.gather 并发执行，总耗时 ≈ 最长 delay。"""
    print("\n--- 并行调用 (gather) ---")
    t0 = time.perf_counter()
    tasks = [
        fetch_data("OpenAI", 1.0),
        fetch_data("Qwen", 1.0),
        fetch_data("DeepSeek", 1.0),
    ]
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - t0
    print(f"并行总耗时: {elapsed:.2f}s")
    return results


async def async_retry_demo() -> None:
    """异步版重试逻辑（理解即可，Day 15 会结合 aiohttp）。"""
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            await fetch_data("flaky_api", 0.3)
            break
        except Exception:
            if attempt == max_attempts:
                raise
            await asyncio.sleep(0.5 * attempt)


def run_async_main() -> None:
    """
    同步入口调用异步主函数的标准写法。
    asyncio.run() 创建事件循环并运行顶层协程。
    """
    print("=" * 50)
    print("Day 13: asyncio 异步演示")
    print("=" * 50)

    async def main() -> None:
        await fetch_sequential()
        await fetch_parallel()
        await async_retry_demo()

    asyncio.run(main())


if __name__ == "__main__":
    run_async_main()
