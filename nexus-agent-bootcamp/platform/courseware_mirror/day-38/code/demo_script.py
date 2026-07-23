#!/usr/bin/env python3
"""Day 38: 答辩演示脚本"""
import subprocess
import sys

STEPS = [
  ("入库", [sys.executable, "enterprise_kb/ingest.py"]),
  ("问答", [sys.executable, "enterprise_kb/retriever.py"]),
]

def main() -> None:
  print("=== Nexus 企业知识库答辩 Demo ===")
  for name, cmd in STEPS:
    print(f"\n>> {name}")
    subprocess.run(cmd, check=False)

if __name__ == "__main__":
  main()
