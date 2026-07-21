"""cli_chat_assistant 配置模块 —— 集中管理环境变量与默认值。"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# 加载项目根目录或当前目录的 .env
load_dotenv()


@dataclass
class AppConfig:
    """
    应用配置数据类。
    所有魔法字符串集中在此，便于测试与部署时覆盖。
    """

    # LLM 相关
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    base_url: str = field(default_factory=lambda: os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o-mini"))
    system_prompt: str = "你是智链科技 NexusAgent 平台的 AI 助手，回答简洁、专业、友好。"
    timeout: int = 30
    mock_mode: bool = False

    # 存储相关
    history_dir: Path = field(default_factory=lambda: Path("data/history"))
    default_save_name: str = "session.json"

    def __post_init__(self) -> None:
        """根据 api_key 自动判断是否 Mock 模式。"""
        key = self.api_key.strip()
        if not key or key.startswith("sk-your") or key == "mock":
            self.mock_mode = True
        self.history_dir.mkdir(parents=True, exist_ok=True)


def get_config() -> AppConfig:
    """获取全局配置单例（简化版，未用真正的单例模式）。"""
    return AppConfig()
