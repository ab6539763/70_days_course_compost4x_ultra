#!/usr/bin/env python3
"""
Day 12 示例：首次 LLM API 调用 —— requests + python-dotenv

演示如何通过 HTTP 调用大模型 API。支持：
  1. 真实 API（配置 .env 中的 API_KEY）
  2. Mock 模式（无密钥时自动降级，课堂可离线演示）
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any

# 第三方库：pip install requests python-dotenv
try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("请先安装依赖: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)

# 加载 .env 文件（若存在）到环境变量
load_dotenv()

# ---------- 配置区 ----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
TIMEOUT_SECONDS = 30


def is_mock_mode() -> bool:
    """判断是否使用 Mock 模式（未配置有效 API Key）。"""
    key = OPENAI_API_KEY.strip()
    return not key or key.startswith("sk-your") or key == "mock"


def mock_chat_completion(messages: list[dict[str, str]], model: str) -> dict[str, Any]:
    """
    Mock 响应，结构与 OpenAI Chat Completions API 一致。
    课堂无网络/无密钥时可正常运行。
    """
    last_user = next(
        (m["content"] for m in reversed(messages) if m["role"] == "user"),
        "（空）",
    )
    return {
        "id": "chatcmpl-mock-day12",
        "object": "chat.completion",
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": (
                        f"[Mock 模式] 你好！我收到了你的消息：「{last_user}」\n"
                        f"配置真实 OPENAI_API_KEY 后即可调用线上模型。"
                    ),
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 30,
            "total_tokens": 50,
        },
    }


def call_openai_chat(
    messages: list[dict[str, str]],
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
) -> dict[str, Any]:
    """
    调用 OpenAI 兼容 Chat Completions API。

    Args:
        messages: [{"role": "user", "content": "..."}]
        model: 模型名称
        temperature: 采样温度 0-2

    Returns:
        API 响应 JSON 字典

    Raises:
        requests.HTTPError: HTTP 状态码非 2xx
        requests.Timeout: 请求超时
    """
    if is_mock_mode():
        print(">>> [提示] 当前为 Mock 模式，未配置有效 API Key", file=sys.stderr)
        return mock_chat_completion(messages, model)

    url = f"{OPENAI_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    # POST 请求，设置超时防止挂起
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=TIMEOUT_SECONDS,
    )
    # 4xx/5xx 时抛出异常，附带响应体便于调试
    response.raise_for_status()
    return response.json()


def extract_reply(response: dict[str, Any]) -> str:
    """从 API 响应中提取助手回复文本。"""
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise ValueError(f"无法解析 API 响应: {response}") from e


def print_usage(response: dict[str, Any]) -> None:
    """打印 Token 用量，企业场景需做成本核算。"""
    usage = response.get("usage", {})
    if usage:
        print(
            f"  [Token] prompt={usage.get('prompt_tokens', '?')} "
            f"completion={usage.get('completion_tokens', '?')} "
            f"total={usage.get('total_tokens', '?')}"
        )


def main() -> None:
    """交互式单次问答演示。"""
    print("=" * 50)
    print("Day 12: 首次 LLM API 调用")
    print(f"模型: {DEFAULT_MODEL}  |  Mock: {is_mock_mode()}")
    print("=" * 50)

    user_input = input("\n请输入问题（直接回车使用默认）: ").strip()
    if not user_input:
        user_input = "用三句话介绍什么是 NexusAgent 智能体平台。"

    messages = [
        {"role": "system", "content": "你是智链科技 Nexus 项目的 AI 助手，回答简洁专业。"},
        {"role": "user", "content": user_input},
    ]

    print("\n正在请求 API...")
    try:
        resp = call_openai_chat(messages)
        reply = extract_reply(resp)
        print("\n助手回复:")
        print("-" * 40)
        print(reply)
        print("-" * 40)
        print_usage(resp)
    except requests.HTTPError as e:
        print(f"HTTP 错误: {e}", file=sys.stderr)
        if e.response is not None:
            print(e.response.text[:500], file=sys.stderr)
        sys.exit(1)
    except requests.Timeout:
        print(f"请求超时（>{TIMEOUT_SECONDS}s）", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
