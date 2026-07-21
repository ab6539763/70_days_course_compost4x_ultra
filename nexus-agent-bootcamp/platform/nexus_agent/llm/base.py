"""LLM 抽象基类 — Day9 继承体系企业版"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Optional


class BaseLLM(ABC):
    """所有大模型客户端的抽象接口"""

    def __init__(self, model: str, api_key: str, base_url: str, **kwargs: Any) -> None:
        self.model = model
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.extra = kwargs

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """同步对话，返回 assistant 文本"""

    @abstractmethod
    async def achat(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """异步对话"""

    def stream_chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> AsyncIterator[str]:
        """流式输出 — 子类可覆盖"""
        raise NotImplementedError("子类需实现 stream_chat")
