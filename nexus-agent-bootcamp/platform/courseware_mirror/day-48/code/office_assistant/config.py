#!/usr/bin/env python3
"""多 Agent 办公助手 — 配置"""
import os
from pathlib import Path

DATA_DIR = Path("data")
LLM_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
API_BASE = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MAX_ITERATIONS = 8
