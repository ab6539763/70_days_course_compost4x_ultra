#!/usr/bin/env python3
"""Day 50: Phase 4 答辩总演示"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "office_assistant"

DEMOS = [
  ("办公助手-写邮件", [sys.executable, str(ROOT / "main.py"), "写项目周报邮件"]),
  ("办公助手-排会议", [sys.executable, str(ROOT / "main.py"), "安排下周评审会议"]),
  ("Text2SQL", [sys.executable, "text2sql.py"]),
]

def main() -> None:
  print("=== Nexus Phase 4 毕业答辩 Demo ===")
  for name, cmd in DEMOS:
    print(f"\n>> {name}")
    subprocess.run(cmd, cwd=Path(__file__).parent, check=False)

if __name__ == "__main__":
  main()
