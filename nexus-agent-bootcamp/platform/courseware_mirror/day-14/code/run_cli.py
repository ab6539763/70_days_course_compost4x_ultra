#!/usr/bin/env python3
"""Day 14 快速启动脚本。"""
import sys
from pathlib import Path

# 将 code/ 加入 path，确保包可导入
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cli_chat_assistant.main import main

if __name__ == "__main__":
    raise SystemExit(main())
