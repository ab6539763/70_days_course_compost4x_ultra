#!/usr/bin/env python3
"""
Day 8 示例：ChatMessage 类 —— 对话消息的领域模型

在企业级大模型应用中，每一条用户/助手消息都需要被结构化存储，
以便后续做历史记录、Token 统计、审计日志等。本模块定义最基础的消息实体。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class MessageRole(str, Enum):
    """消息角色枚举，与 OpenAI Chat Completions API 的 role 字段对齐。"""

    SYSTEM = "system"      # 系统提示词，设定 AI 行为
    USER = "user"          # 终端用户输入
    ASSISTANT = "assistant"  # 模型回复
    TOOL = "tool"          # 工具调用结果（Day 40+ 会用到）


@dataclass
class ChatMessage:
    """
    单条聊天消息的领域对象。

    属性:
        role: 消息角色（system/user/assistant/tool）
        content: 消息正文，纯文本
        timestamp: 消息创建时间，默认取当前时间
        metadata: 扩展字段，如 token 数、模型名称、trace_id 等
    """

    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """构造后校验：确保 role 为枚举类型、content 非空。"""
        # 允许传入字符串形式的 role，自动转换为枚举
        if isinstance(self.role, str):
            self.role = MessageRole(self.role)
        if not self.content or not self.content.strip():
            raise ValueError("消息内容 content 不能为空")

    def to_dict(self) -> dict[str, Any]:
        """序列化为字典，便于 JSON 存储或 API 传输。"""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChatMessage:
        """从字典反序列化，用于读取历史记录文件。"""
        ts = data.get("timestamp")
        if isinstance(ts, str):
            timestamp = datetime.fromisoformat(ts)
        else:
            timestamp = datetime.now()
        return cls(
            role=MessageRole(data["role"]),
            content=data["content"],
            timestamp=timestamp,
            metadata=data.get("metadata", {}),
        )

    def word_count(self) -> int:
        """粗略统计字数（中文按字符、英文按空格分词）。"""
        # 简单实现：去除首尾空白后按空白切分
        return len(self.content.split())

    def preview(self, max_len: int = 50) -> str:
        """生成消息预览，用于 CLI 历史列表展示。"""
        text = self.content.replace("\n", " ")
        if len(text) <= max_len:
            return text
        return text[: max_len - 3] + "..."

    def __repr__(self) -> str:
        return (
            f"ChatMessage(role={self.role.value!r}, "
            f"content={self.preview(30)!r}, "
            f"timestamp={self.timestamp:%Y-%m-%d %H:%M})"
        )


def demo() -> None:
    """演示 ChatMessage 的基本用法。"""
    # 1. 创建用户消息
    user_msg = ChatMessage(role=MessageRole.USER, content="你好，请介绍一下 NexusAgent 平台。")
    print("用户消息:", user_msg)
    print("字数:", user_msg.word_count())

    # 2. 创建助手回复，附带 metadata
    assistant_msg = ChatMessage(
        role=MessageRole.ASSISTANT,
        content="NexusAgent 是智链科技的企业级智能体协作平台，支持多轮对话与知识库问答。",
        metadata={"model": "qwen-plus", "tokens": 42},
    )
    print("助手消息:", assistant_msg)

    # 3. 序列化与反序列化
    payload = user_msg.to_dict()
    restored = ChatMessage.from_dict(payload)
    print("反序列化成功:", restored.role == user_msg.role)

    # 4. 批量消息列表（后续 Day 14 会用于对话历史）
    history: list[ChatMessage] = [user_msg, assistant_msg]
    print(f"\n对话历史共 {len(history)} 条:")
    for i, msg in enumerate(history, 1):
        print(f"  [{i}] {msg.role.value}: {msg.preview()}")


if __name__ == "__main__":
    demo()
