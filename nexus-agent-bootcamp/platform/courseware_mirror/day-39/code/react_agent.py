#!/usr/bin/env python3
"""Day 39: 手写 ReAct Agent"""
import re
from tools import TOOLS

SYSTEM = """你是助手，使用以下格式：
Thought: 思考
Action: 工具名[参数]
Observation: 工具返回
... 最终 Answer: 结论
可用工具: search, calculator
"""

def parse_action(text: str) -> tuple[str, str] | None:
  m = re.search(r"Action:\s*(\w+)\[(.*?)\]", text, re.DOTALL)
  return (m.group(1), m.group(2)) if m else None

def react_loop(question: str, max_steps: int = 5) -> str:
  history = SYSTEM + f"\nQuestion: {question}\n"
  for _ in range(max_steps):
    # 教学 mock：规则生成 Thought/Action
    if "计算" in question or "+" in question:
      thought = "Thought: 需要计算\nAction: calculator[2+3]\n"
    else:
      thought = "Thought: 需要搜索\nAction: search[Nexus RAG]\n"
    history += thought
    action = parse_action(thought)
    if not action:
      break
    name, arg = action
    obs = TOOLS[name](arg)
    history += f"Observation: {obs}\n"
    if "Answer:" in obs:
      return obs
  return history + "Answer: 未能在限定步数内完成"

if __name__ == "__main__":
  print(react_loop("Nexus 用什么做 RAG？"))
  print(react_loop("计算 2+3"))
