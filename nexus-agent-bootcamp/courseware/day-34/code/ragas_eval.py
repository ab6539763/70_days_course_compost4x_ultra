#!/usr/bin/env python3
"""Day 34: Ragas 评估（可选依赖，无则 mock）"""
from dataclasses import dataclass

@dataclass
class RagSample:
  question: str
  answer: str
  contexts: list[str]
  ground_truth: str

def faithfulness(answer: str, contexts: list[str]) -> float:
  # 答案是否可由上下文推出
  ctx = " ".join(contexts)
  overlap = sum(1 for w in answer.split() if w in ctx)
  return min(overlap / max(len(answer.split()), 1), 1.0)

def answer_relevancy(answer: str, question: str) -> float:
  overlap = sum(1 for w in question.split() if w in answer)
  return min(overlap / max(len(question.split()), 1), 1.0)

if __name__ == "__main__":
  s = RagSample("年假几天", "5天年假", ["工作满一年享5天年假"], "5天")
  print("faithfulness:", faithfulness(s.answer, s.contexts))
  print("relevancy:", answer_relevancy(s.answer, s.question))
