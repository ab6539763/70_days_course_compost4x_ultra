#!/usr/bin/env python3
"""Day 43: 多 Agent 消息传递"""
from dataclasses import dataclass, field

@dataclass
class Agent:
  name: str
  role: str

  def run(self, task: str, context: str = "") -> str:
    return f"[{self.name}/{self.role}] 处理: {task} | 上下文: {context[:50]}"

@dataclass
class Team:
  agents: list[Agent] = field(default_factory=list)

  def delegate(self, task: str) -> str:
    results = []
    ctx = ""
    for a in self.agents:
      out = a.run(task, ctx)
      results.append(out)
      ctx += out + "\n"
    return "\n".join(results)

if __name__ == "__main__":
  team = Team([Agent("researcher", "检索"), Agent("writer", "写作")])
  print(team.delegate("写一份 RAG 技术简报"))
