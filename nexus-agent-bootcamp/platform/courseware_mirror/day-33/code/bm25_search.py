#!/usr/bin/env python3
"""Day 33: 简易 BM25 关键词检索"""
import math
from collections import Counter

def bm25_score(query: str, doc: str, avgdl: float = 100, k1: float = 1.5, b: float = 0.75) -> float:
  q_terms = query.split()
  d_terms = doc.split()
  dl = len(d_terms)
  tf = Counter(d_terms)
  score = 0.0
  for t in q_terms:
    if t in tf:
      freq = tf[t]
      score += (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * dl / avgdl))
  return score

CORPUS = ["年假 5 天 工作满一年", "报销 需要 发票 30 日", "远程 办公 需 申请"]

if __name__ == "__main__":
  q = "年假"
  ranked = sorted(CORPUS, key=lambda d: bm25_score(q, d), reverse=True)
  print(ranked)
