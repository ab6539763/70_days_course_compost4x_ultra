"""cli_chat_assistant LLM 客户端 —— 封装 API 调用与 Mock。"""
from __future__ import annotations

from typing import Any

import requests

from cli_chat_assistant.config import AppConfig


def mock_completion(messages: list[dict[str, str]], model: str) -> dict[str, Any]:
    """
    Mock 模式响应，无需真实 API Key 即可演示完整 CLI 流程。
    会根据用户最后一条消息生成模板回复。
    """
    last_user = ""
    for m in reversed(messages):
        if m["role"] == "user":
            last_user = m["content"]
            break

    # 简单关键词回复，增加演示趣味性
    if "你好" in last_user or "hello" in last_user.lower():
        reply = "你好！我是 NexusAgent CLI 助手，有什么可以帮您？"
    elif "rag" in last_user.lower() or "检索" in last_user:
        reply = "RAG（检索增强生成）通过向量检索相关知识再生成回答，是 Day 25+ 的核心内容。"
    elif "/help" in last_user:
        reply = "输入普通文本即可对话。内置命令: /clear /save /exit /help"
    else:
        reply = (
            f"[Mock/{model}] 收到您的消息（{len(last_user)} 字）：\n"
            f"「{last_user[:80]}{'...' if len(last_user) > 80 else ''}」\n"
            f"配置 OPENAI_API_KEY 后可获得真实 AI 回复。"
        )

    return {
        "choices": [{"message": {"role": "assistant", "content": reply}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        "model": model,
    }


def chat_completion(messages: list[dict[str, str]], config: AppConfig) -> str:
    """
    发送多轮对话请求，返回助手回复文本。

    Args:
        messages: OpenAI 格式的消息列表
        config: 应用配置

    Returns:
        助手回复的纯文本

    Raises:
        requests.RequestException: 网络或 HTTP 错误
    """
    if config.mock_mode:
        resp = mock_completion(messages, config.model)
        return resp["choices"][0]["message"]["content"]

    url = f"{config.base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config.model,
        "messages": messages,
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=config.timeout)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
