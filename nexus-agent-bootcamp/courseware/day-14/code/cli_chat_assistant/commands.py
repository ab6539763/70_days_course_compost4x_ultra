"""cli_chat_assistant 内置斜杠命令处理。"""
from __future__ import annotations

from pathlib import Path

from cli_chat_assistant.config import AppConfig
from cli_chat_assistant.models import ChatSession
from cli_chat_assistant.storage import list_saved_sessions, save_session

# 所有支持的斜杠命令
BUILTIN_COMMANDS = ("/clear", "/save", "/exit", "/help", "/history")


def is_command(text: str) -> bool:
    """判断输入是否为斜杠命令。"""
    return text.strip().startswith("/")


def handle_command(text: str, session: ChatSession, config: AppConfig) -> tuple[bool, str]:
    """
    处理斜杠命令。

    Returns:
        (should_exit, message)
        - should_exit: True 表示应退出主循环
        - message: 反馈给用户的文本（空串表示无需额外输出）
    """
    cmd = text.strip().lower()
    parts = cmd.split(maxsplit=1)
    command = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    if command == "/exit":
        return True, "再见！感谢使用 NexusAgent CLI 助手。"

    if command == "/clear":
        count = session.clear()
        return False, f"已清空 {count} 条对话记录（系统提示词保留）。"

    if command == "/save":
        # /save 或 /save my_session.json
        filename = arg.strip() if arg else config.default_save_name
        if not filename.endswith(".json"):
            filename += ".json"
        path = config.history_dir / filename
        save_session(session, path)
        return False, f"会话已保存至 {path}（共 {session.message_count()} 条消息）。"

    if command == "/history":
        lines = [f"--- 当前会话 {session.session_id} ---"]
        for i, msg in enumerate(session.messages, 1):
            lines.append(f"  {i}. [{msg.role.value}] {msg.preview(50)}")
        if not session.messages:
            lines.append("  （暂无消息）")
        saved = list_saved_sessions(config.history_dir)
        if saved:
            lines.append(f"\n已保存文件 ({len(saved)} 个):")
            for p in saved[-5:]:
                lines.append(f"  - {p.name}")
        return False, "\n".join(lines)

    if command == "/help":
        help_text = """
可用命令:
  /clear          清空当前对话历史
  /save [文件名]   保存会话到 data/history/
  /history        查看当前会话消息列表
  /help           显示此帮助
  /exit           退出程序

直接输入文字即可与 AI 对话。
"""
        return False, help_text.strip()

    return False, f"未知命令: {command}，输入 /help 查看帮助。"
