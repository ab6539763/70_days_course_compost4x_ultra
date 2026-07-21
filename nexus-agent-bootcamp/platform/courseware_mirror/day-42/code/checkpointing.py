#!/usr/bin/env python3
"""Day 42: MemorySaver 检查点"""
from langgraph.checkpoint.memory import MemorySaver
from state_graph import app as base_app

memory = MemorySaver()
app = base_app  # 教学：编译时 checkpointer=memory

if __name__ == "__main__":
  config = {"configurable": {"thread_id": "session-1"}}
  print("Checkpoint 演示 thread_id=session-1")
