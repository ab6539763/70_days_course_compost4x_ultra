#!/usr/bin/env python3
"""多 Agent 办公助手 — CLI 入口"""
import argparse
from graph.workflow import build_graph

def main() -> None:
  parser = argparse.ArgumentParser(description="Nexus 办公助手")
  parser.add_argument("task", help="办公任务描述")
  args = parser.parse_args()
  app = build_graph()
  result = app.invoke({"task": args.task, "route": "", "context": "", "output": ""})
  print("=== 办公助手输出 ===")
  print(result["output"])

if __name__ == "__main__":
  main()
