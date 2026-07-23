#!/usr/bin/env python3
"""Day 27: 会话 ID 与内存字典模拟 Redis"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ChatSession:
  session_id: str
  messages: list[dict[str, str]] = field(default_factory=list)

  def append(self, role: str, content: str) -> None:
    self.messages.append({"role": role, "content": content})

  def context_text(self, max_turns: int = 10) -> str:
    # 只保留最近 max_turns 轮，防止 token 爆炸
    recent = self.messages[-(max_turns * 2):]
    return "\n".join(f"{m['role']}: {m['content']}" for m in recent)

SESSION_STORE: dict[str, ChatSession] = {}

def get_session(sid: str) -> ChatSession:
  if sid not in SESSION_STORE:
    SESSION_STORE[sid] = ChatSession(session_id=sid)
  return SESSION_STORE[sid]

if __name__ == "__main__":
  s = get_session("user-001")
  s.append("user", "Nexus 支持私有化吗？")
  s.append("assistant", "支持 Docker 私有化部署。")
  print(s.context_text())
