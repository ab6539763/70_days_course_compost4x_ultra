#!/usr/bin/env python3
"""
Day 9 示例：BaseModel 抽象基类 —— 统一大模型调用接口

企业里往往对接多家模型供应商（OpenAI、通义千问、DeepSeek 等），
通过继承抽象出统一接口，上层业务代码无需关心具体厂商实现。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModelResponse:
    """模型调用的统一响应结构。"""

    content: str
    model_name: str
    usage: dict[str, int] = field(default_factory=dict)  # prompt_tokens, completion_tokens 等
    raw: dict[str, Any] = field(default_factory=dict)    # 原始 API 响应，调试用


class BaseModel(ABC):
    """
    大语言模型抽象基类。

    子类必须实现 chat() 方法。基类提供公共属性与工具方法。
    """

    def __init__(self, model_name: str, api_key: str = "", **kwargs: Any) -> None:
        self.model_name = model_name
        self.api_key = api_key
        self.extra_config = kwargs

    @abstractmethod
    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> ModelResponse:
        """
        发送多轮对话请求。

        Args:
            messages: [{"role": "user", "content": "..."}, ...]
        Returns:
            ModelResponse 统一响应对象
        """
        ...

    def validate_messages(self, messages: list[dict[str, str]]) -> None:
        """校验消息列表格式，子类可在 chat 开头调用。"""
        if not messages:
            raise ValueError("messages 不能为空")
        for msg in messages:
            if "role" not in msg or "content" not in msg:
                raise ValueError(f"消息缺少 role 或 content: {msg}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model_name!r})"
