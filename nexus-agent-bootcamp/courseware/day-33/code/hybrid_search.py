#!/usr/bin/env python3
"""Day 33: 向量 + BM25 混合检索"""
from bm25_search import bm25_score, CORPUS

def dense_score(query: str, doc: str) -> float:
  # 教学 mock：字符重叠
  return sum(1 for c in query if c in doc) / max(len(query), 1)

def hybrid_search(query: str, alpha: float = 0.5) -> list[tuple[str, float]]:
  results = []
  for doc in CORPUS:
    s = alpha * dense_score(query, doc) + (1 - alpha) * bm25_score(query, doc)
    results.append((doc, s))
  return sorted(results, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
  for doc, s in hybrid_search("年假政策", alpha=0.6):
    print(f"{s:.3f} {doc}")
