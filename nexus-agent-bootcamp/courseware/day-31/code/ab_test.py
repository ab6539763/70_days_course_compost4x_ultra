#!/usr/bin/env python3
"""Day 31: A/B 测试记录"""
import json
from pathlib import Path

def log_result(variant: str, query: str, answer: str, score: float) -> None:
  p = Path("logs/ab_test.jsonl")
  p.parent.mkdir(exist_ok=True)
  with p.open("a", encoding="utf-8") as f:
    f.write(json.dumps({"variant": variant, "query": query, "answer": answer, "score": score}, ensure_ascii=False) + "\n")

if __name__ == "__main__":
  log_result("A_k2", "年假", "5天", 0.9)
  log_result("B_k5", "年假", "5天年假", 0.85)
