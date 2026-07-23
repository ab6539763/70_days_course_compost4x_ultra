#!/usr/bin/env python3
"""
cli_chat_assistant 主入口 —— 多轮对话 REPL

运行方式（在 code/ 目录下）:
    python -m cli_chat_assistant

或:
    python cli_chat_assistant/main.py
"""
from __future__ import annotations

import sys
import uuid
from datetime import datetime

from cli_chat_assistant.commands import handle_command, is_command
from cli_chat_assistant.config import get_config
from cli_chat_assistant.llm_client import chat_completion
from cli_chat_assistant.models import ChatSession


def print_banner(config) -> None:
    """打印启动横幅与模式提示。"""
    mode = "Mock 模式（无 API Key）" if config.mock_mode else f"在线模式 ({config.model})"
    print("=" * 56)
    print("  NexusAgent CLI 助手  |  阶段项目一  |  Day 14")
    print("  智链科技 SmartLink Tech")
    print("=" * 56)
    print(f"  会话模式: {mode}")
    print("  输入 /help 查看命令，/exit 退出")
    print("=" * 56)


def create_session(config) -> ChatSession:
    """创建新会话，生成唯一 session_id。"""
    sid = f"sess-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:8]}"
    return ChatSession(
        session_id=sid,
        system_prompt=config.system_prompt,
    )


def read_user_input() -> str | None:
    """
    读取用户输入，处理 EOF（Ctrl+D） gracefully。
    Returns None 表示用户请求退出。
    """
    try:
        return input("\n你> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n")
        return None


def run_chat_loop() -> int:
    """主对话循环，返回进程退出码。"""
    config = get_config()
    session = create_session(config)
    print_banner(config)

    while True:
        user_text = read_user_input()

        # EOF / Ctrl+C 视为退出
        if user_text is None:
            print("再见！")
            return 0

        if not user_text:
            continue

        # ---------- 斜杠命令分支 ----------
        if is_command(user_text):
            should_exit, msg = handle_command(user_text, session, config)
            if msg:
                print(msg)
            if should_exit:
                return 0
            continue

        # ---------- 普通对话分支 ----------
        session.add_user(user_text)
        api_messages = session.build_api_messages()

        print("助手> ", end="", flush=True)
        try:
            reply = chat_completion(api_messages, config)
            print(reply)
            session.add_assistant(reply)
        except Exception as e:
            # 请求失败时回滚刚添加的用户消息，保持历史一致
            session.messages.pop()
            print(f"\n[错误] API 调用失败: {e}", file=sys.stderr)
            print("请检查网络与 API Key 配置，或稍后重试。", file=sys.stderr)

    return 0


def main() -> int:
    """程序入口。"""
    return run_chat_loop()


if __name__ == "__main__":
    raise SystemExit(main())
