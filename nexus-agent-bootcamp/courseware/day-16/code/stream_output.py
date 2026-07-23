#!/usr/bin/env python3
"""
Day 16 实操：流式输出（Streaming）
演示 SSE 风格逐 token 打印，模拟 ChatGPT 打字机效果。
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")


def mock_stream(text: str, delay: float = 0.03) -> None:
    """无 API 时的模拟流式输出。"""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def stream_chat(prompt: str) -> None:
    """流式调用 Chat API 并实时打印。"""
    if not API_KEY:
        mock_stream(
            "【MOCK 流式】NexusAgent 平台通过 REST API 与 SSE "
            "为前端提供实时对话能力，是 Day 22-24 的前置基础。"
        )
        return

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "temperature": 0.7,
    }
    req = urllib.request.Request(
        f"{API_BASE}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        method="POST",
    )

    print("助手: ", end="", flush=True)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8").strip()
                if not line or not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        sys.stdout.write(content)
                        sys.stdout.flush()
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
        print()
    except urllib.error.URLError as exc:
        print(f"\n[ERROR] 流式请求失败: {exc}")


def main() -> None:
    prompt = "用三句话解释什么是 Server-Sent Events（SSE）。"
    print("=" * 60)
    print("Day 16 — 流式输出演示")
    print("=" * 60)
    print(f"用户: {prompt}\n")
    stream_chat(prompt)


if __name__ == "__main__":
    main()
