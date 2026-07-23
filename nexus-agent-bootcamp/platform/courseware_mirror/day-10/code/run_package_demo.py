#!/usr/bin/env python3
"""
Day 10 演示：以包方式运行 nexus_cli

在 code/ 目录下执行:
    python -m nexus_cli greet 张三
    python -m nexus_cli version
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=CODE_DIR, check=False)
    print()


if __name__ == "__main__":
    py = sys.executable
    run([py, "-m", "nexus_cli", "greet", "林悦"])
    run([py, "-m", "nexus_cli", "version"])
    # 触发 ValidationError
    run([py, "-m", "nexus_cli", "greet", ""])
