#!/usr/bin/env python3
"""Day 32: 简易 Reranker — 按关键词重叠重排"""
from dataclasses import dataclass

@dataclass
class Doc:
  text: str
  score: float = 0.0

def rerank(query: str, docs: list[Doc]) -> list[Doc]:
  q_tokens = set(query)
  for d in docs:
    d.score = sum(1 for c in q_tokens if c in d.text) / max(len(q_tokens), 1)
  return sorted(docs, key=lambda x: x.score, reverse=True)

if __name__ == "__main__":
  docs = [Doc("年假 5 天"), Doc("报销发票"), Doc("考勤打卡")]
  for d in rerank("年假", docs):
    print(d.score, d.text)
