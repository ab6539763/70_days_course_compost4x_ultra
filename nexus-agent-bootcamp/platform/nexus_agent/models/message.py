"""对话消息模型 — Day8 ChatMessage 企业升级版"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import json


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class ChatMessage:
    role: Role
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_api_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"role": self.role.value, "content": self.content}
        if self.name:
            d["name"] = self.name
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        return d

    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> "ChatMessage":
        return cls(role=Role(data["role"]), content=data.get("content", ""))

    def to_json(self) -> str:
        return json.dumps({
            "role": self.role.value,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }, ensure_ascii=False)


@dataclass
class Conversation:
    """多轮会话 — 支持持久化"""
    id: str
    messages: List[ChatMessage] = field(default_factory=list)
    title: Optional[str] = None

    def add(self, msg: ChatMessage) -> None:
        self.messages.append(msg)

    def to_messages_api(self) -> List[Dict[str, Any]]:
        return [m.to_api_dict() for m in self.messages]

    def clear(self) -> None:
        self.messages.clear()
