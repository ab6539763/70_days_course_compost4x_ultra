#!/usr/bin/env python3
"""
Day 9 示例：QwenModel —— 通义千问模型实现，演示多态

与 OpenAIModel 继承同一基类，上层可用 BaseModel 类型统一调度。
"""
from __future__ import annotations

from typing import Any

from base_model import BaseModel, ModelResponse


class QwenModel(BaseModel):
    """阿里云通义千问 DashScope API 模型实现。"""

    def __init__(
        self,
        model_name: str = "qwen-plus",
        api_key: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(model_name, api_key, **kwargs)

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> ModelResponse:
        """模拟调用通义千问 API。"""
        self.validate_messages(messages)

        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )
        # 通义千问风格的模拟回复
        fake_reply = f"[通义千问/{self.model_name}] 您好！关于「{last_user[:30]}」，我来为您解答。"

        return ModelResponse(
            content=fake_reply,
            model_name=self.model_name,
            usage={"input_tokens": 15, "output_tokens": 25},
            raw={"request_id": "mock-qwen-req-001"},
        )


def demo_polymorphism() -> None:
    """多态演示：同一函数处理不同子类。"""
    from openai_model import OpenAIModel

    models: list[BaseModel] = [
        OpenAIModel("gpt-4o-mini"),
        QwenModel("qwen-plus"),
    ]
    messages = [{"role": "user", "content": "什么是 RAG？"}]

    print("=== 多态调用 demo ===")
    for m in models:
        resp = m.chat(messages)
        print(f"{m} -> {resp.content}")


if __name__ == "__main__":
    demo_polymorphism()
