#!/usr/bin/env python3
"""Day 9 综合演示：模型工厂与多态调度。"""
from __future__ import annotations

from base_model import BaseModel
from openai_model import OpenAIModel
from qwen_model import QwenModel


def create_model(provider: str, **kwargs) -> BaseModel:
    """
    简单工厂：根据 provider 字符串创建对应模型实例。

    企业实践中可扩展为注册表模式（Day 39 Agent 工具注册同理）。
    """
    registry: dict[str, type[BaseModel]] = {
        "openai": OpenAIModel,
        "qwen": QwenModel,
    }
    cls = registry.get(provider.lower())
    if cls is None:
        raise ValueError(f"未知 provider: {provider}，可选: {list(registry)}")
    return cls(**kwargs)


if __name__ == "__main__":
    for provider in ("openai", "qwen"):
        model = create_model(provider, model_name="default")
        r = model.chat([{"role": "user", "content": "讲个笑话"}])
        print(r.content)
