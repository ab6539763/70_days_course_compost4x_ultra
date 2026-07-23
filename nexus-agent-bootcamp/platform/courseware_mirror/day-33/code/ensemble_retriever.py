#!/usr/bin/env python3
"""Day 33: Ensemble Retriever 概念演示"""
from hybrid_search import hybrid_search

class EnsembleRetriever:
  def __init__(self, alpha: float = 0.5):
    self.alpha = alpha

  def invoke(self, query: str, k: int = 3) -> list[str]:
    return [d for d, _ in hybrid_search(query, self.alpha)[:k]]

if __name__ == "__main__":
  r = EnsembleRetriever(0.5)
  print(r.invoke("报销流程"))
