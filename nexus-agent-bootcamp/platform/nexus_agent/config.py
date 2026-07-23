"""全局配置 — 支持环境变量与多环境"""
from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """应用配置，从环境变量读取，带默认值便于本地开发"""
    app_name: str = "NexusAgent"
    debug: bool = False
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./nexus.db"
    redis_url: Optional[str] = None
    llm_provider: str = "deepseek"
    llm_api_key: Optional[str] = None
    llm_base_url: str = "https://api.deepseek.com/v1"
    llm_model: str = "deepseek-chat"
    embedding_model: str = "text-embedding-3-small"
    chroma_persist_dir: str = "./data/chroma"
    max_tokens: int = 4096
    temperature: float = 0.7

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            database_url=os.getenv("DATABASE_URL", "sqlite:///./nexus.db"),
            llm_api_key=os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY"),
            llm_provider=os.getenv("LLM_PROVIDER", "deepseek"),
            llm_model=os.getenv("LLM_MODEL", "deepseek-chat"),
        )


settings = Settings.from_env()
