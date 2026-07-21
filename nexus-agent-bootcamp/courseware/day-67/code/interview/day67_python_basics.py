#!/usr/bin/env python3
"""
Day 67 — Python 面试高频题跟敲
"""
from functools import wraps
from collections import OrderedDict


# --- 1. 装饰器：计时 + 日志 ---
def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {(time.perf_counter()-start)*1000:.1f}ms")
        return result
    return wrapper


# --- 2. 生成器：内存友好的大数据处理 ---
def read_large_file(path: str):
    with open(path) as f:
        for line in f:
            yield line.strip()


# --- 3. LRU Cache 实现（面试手写题）---
class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# --- 4. 异步 FastAPI 依赖注入示例 ---
@timed
def demo_lru():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    print(cache.get(1))
    cache.put(3, "c")
    print(cache.get(2))  # -1


if __name__ == "__main__":
    demo_lru()
