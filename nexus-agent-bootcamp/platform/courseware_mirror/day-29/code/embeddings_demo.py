#!/usr/bin/env python3
"""Day 29: Embedding 向量维度与余弦相似度"""
import math

def cosine(a: list[float], b: list[float]) -> float:
  dot = sum(x * y for x, y in zip(a, b))
  na = math.sqrt(sum(x * x for x in a))
  nb = math.sqrt(sum(x * x for x in b))
  return dot / (na * nb) if na and nb else 0.0

# 教学用伪向量
v1 = [1.0, 0.2, 0.1]
v2 = [0.9, 0.3, 0.0]
v3 = [0.0, 1.0, 0.0]
print("相似问句:", cosine(v1, v2))
print("无关问句:", cosine(v1, v3))
