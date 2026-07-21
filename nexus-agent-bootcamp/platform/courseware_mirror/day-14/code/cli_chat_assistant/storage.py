"""cli_chat_assistant 持久化 —— 会话保存与加载。"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from cli_chat_assistant.models import ChatSession, Message


def session_to_dict(session: ChatSession) -> dict[str, Any]:
    """将会话对象序列化为可 JSON 存储的字典。"""
    return {
        "session_id": session.session_id,
        "system_prompt": session.system_prompt,
        "created_at": session.created_at.isoformat(),
        "messages": [m.to_storage_dict() for m in session.messages],
    }


def session_from_dict(data: dict[str, Any]) -> ChatSession:
    """从字典恢复 ChatSession 对象。"""
    created = data.get("created_at")
    created_at = datetime.fromisoformat(created) if isinstance(created, str) else datetime.now()
    session = ChatSession(
        session_id=data["session_id"],
        system_prompt=data.get("system_prompt", ""),
        created_at=created_at,
    )
    for msg_data in data.get("messages", []):
        session.messages.append(Message.from_storage_dict(msg_data))
    return session


def save_session(session: ChatSession, path: Path) -> None:
    """
    保存会话到 JSON 文件。

    文件格式 UTF-8，缩进 2 空格，便于人工查看与 Git diff。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = session_to_dict(session)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_session(path: Path) -> ChatSession:
    """从 JSON 文件加载会话，文件不存在时抛出 FileNotFoundError。"""
    if not path.exists():
        raise FileNotFoundError(f"会话文件不存在: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return session_from_dict(data)


def list_saved_sessions(history_dir: Path) -> list[Path]:
    """列出历史目录下所有 .json 会话文件。"""
    if not history_dir.exists():
        return []
    return sorted(history_dir.glob("*.json"))
