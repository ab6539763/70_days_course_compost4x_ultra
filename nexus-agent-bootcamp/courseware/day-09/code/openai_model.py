#!/usr/bin/env python3
"""
Day 9 示例：OpenAIModel —— 继承 BaseModel，模拟 OpenAI 兼容接口

实际项目中可替换为真实 requests 调用；本日侧重继承与多态演示。
"""
from __future__ import annotations

from typing import Any

from base_model import BaseModel, ModelResponse


class OpenAIModel(BaseModel):
    """OpenAI 及兼容 API（如 DeepSeek）的模型实现。"""

    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        api_key: str = "",
        base_url: str = "https://api.openai.com/v1",
        **kwargs: Any,
    ) -> None:
        super().__init__(model_name, api_key, **kwargs)
        self.base_url = base_url

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> ModelResponse:
        """模拟调用 OpenAI Chat Completions API。"""
        self.validate_messages(messages)

        # 模拟 API 响应（Day 12 会改为真实 HTTP 请求）
        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )
        fake_reply = f"[OpenAI/{self.model_name}] 收到: {last_user[:50]}"

        return ModelResponse(
            content=fake_reply,
            model_name=self.model_name,
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            raw={"id": "chatcmpl-mock-openai", "object": "chat.completion"},
        )


if __name__ == "__main__":
    model = OpenAIModel(model_name="gpt-4o-mini", api_key="sk-mock")
    resp = model.chat([{"role": "user", "content": "你好"}])
    print(resp.content)
    print("usage:", resp.usage)
