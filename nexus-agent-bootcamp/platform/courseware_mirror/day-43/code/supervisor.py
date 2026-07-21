#!/usr/bin/env python3
"""Day 43: Supervisor 调度"""
from multi_agent import Agent

class Supervisor:
  def __init__(self, workers: dict[str, Agent]):
    self.workers = workers

  def route(self, task: str) -> str:
    if "搜索" in task or "检索" in task:
      return self.workers["researcher"].run(task)
    if "写" in task or "报告" in task:
      return self.workers["writer"].run(task)
    return self.workers["researcher"].run(task)

if __name__ == "__main__":
  sup = Supervisor({
    "researcher": Agent("R", "检索"),
    "writer": Agent("W", "写作"),
  })
  print(sup.route("写项目周报"))
