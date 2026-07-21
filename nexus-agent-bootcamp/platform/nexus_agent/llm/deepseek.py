"""DeepSeek API 客户端"""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional
import urllib.request


class DeepSeekLLM:
    """DeepSeek 兼容 OpenAI Chat Completions 格式"""

    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-chat") -> None:
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.model = model
        self.base_url = "https://api.deepseek.com/v1"

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 2048) -> str:
        if not self.api_key:
            return "[MOCK] DeepSeek 未配置 API Key，返回模拟回复"
        body = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"]
