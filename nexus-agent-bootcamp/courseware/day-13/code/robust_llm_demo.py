#!/usr/bin/env python3
"""
Day 13 综合：将 retry 装饰器应用于 Day 12 API 调用（同步版）
"""
from __future__ import annotations

import sys
from pathlib import Path

# 允许从同级目录导入 Day 12 模块
sys.path.insert(0, str(Path(__file__).resolve().parent))

from retry_decorator import retry

try:
    import requests
    from first_llm_call import call_openai_chat, extract_reply
except ImportError:
    print("请确保 first_llm_call.py 在同目录")
    sys.exit(1)


@retry(max_attempts=3, delay=2.0, exceptions=(requests.RequestException,))
def robust_chat(prompt: str) -> str:
    """带重试的单轮对话封装。"""
    messages = [{"role": "user", "content": prompt}]
    resp = call_openai_chat(messages)
    return extract_reply(resp)


if __name__ == "__main__":
    reply = robust_chat("async 和 sync 有什么区别？用一句话回答。")
    print(reply)
