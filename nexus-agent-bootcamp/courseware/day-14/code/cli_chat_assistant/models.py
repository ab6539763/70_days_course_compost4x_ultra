"""cli_chat_assistant 领域模型 —— 消息与对话会话。"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Role(str, Enum):
    """消息角色，与 OpenAI API 对齐。"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """单条对话消息。"""

    role: Role
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_api_dict(self) -> dict[str, str]:
        """转换为 LLM API 所需的 {role, content} 格式。"""
        return {"role": self.role.value, "content": self.content}

    def to_storage_dict(self) -> dict[str, Any]:
        """转换为可 JSON 序列化的完整字典。"""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_storage_dict(cls, data: dict[str, Any]) -> Message:
        """从持久化数据恢复 Message 对象。"""
        ts = data.get("timestamp")
        timestamp = datetime.fromisoformat(ts) if isinstance(ts, str) else datetime.now()
        return cls(role=Role(data["role"]), content=data["content"], timestamp=timestamp)

    def preview(self, max_len: int = 60) -> str:
        """生成简短预览，用于历史列表。"""
        text = self.content.replace("\n", " ")
        return text if len(text) <= max_len else text[: max_len - 3] + "..."


@dataclass
class ChatSession:
    """
    一次完整的对话会话，包含系统提示词与多轮消息历史。
  Day 8 ChatMessage 的升级版，增加了会话级管理。
    """

    session_id: str
    messages: list[Message] = field(default_factory=list)
    system_prompt: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def add_user(self, content: str) -> Message:
        """添加用户消息并返回。"""
        msg = Message(role=Role.USER, content=content)
        self.messages.append(msg)
        return msg

    def add_assistant(self, content: str) -> Message:
        """添加助手回复并返回。"""
        msg = Message(role=Role.ASSISTANT, content=content)
        self.messages.append(msg)
        return msg

    def clear(self) -> int:
        """清空对话历史（保留 system），返回清除条数。"""
        count = len(self.messages)
        self.messages.clear()
        return count

    def build_api_messages(self) -> list[dict[str, str]]:
        """
        构建发送给 LLM API 的 messages 数组。
        格式: [system, user, assistant, user, assistant, ...]
        """
        result: list[dict[str, str]] = []
        if self.system_prompt:
            result.append({"role": "system", "content": self.system_prompt})
        for msg in self.messages:
            result.append(msg.to_api_dict())
        return result

    def message_count(self) -> int:
        """返回当前消息条数。"""
        return len(self.messages)

    def last_exchange_preview(self) -> str:
        """返回最近一轮问答的预览文本。"""
        if not self.messages:
            return "（空会话）"
        last = self.messages[-1]
        return f"[{last.role.value}] {last.preview()}"
