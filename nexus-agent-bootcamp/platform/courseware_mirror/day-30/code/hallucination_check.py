#!/usr/bin/env python3
"""Day 30: 简单幻觉检测 — 答案是否包含上下文关键词"""

def grounded(answer: str, context: str, min_overlap: int = 2) -> bool:
  # 教学用启发式：答案中至少 min_overlap 个上下文词出现
  tokens = [t for t in context.split() if len(t) > 1]
  hits = sum(1 for t in set(tokens) if t in answer)
  return hits >= min_overlap

if __name__ == "__main__":
  ctx = "年假 5 天 工作满一年"
  print(grounded("工作满一年有 5 天年假", ctx))
  print(grounded("无限年假随便休", ctx))
