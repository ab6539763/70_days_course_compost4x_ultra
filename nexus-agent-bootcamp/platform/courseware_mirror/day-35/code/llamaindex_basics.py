#!/usr/bin/env python3
"""Day 35: LlamaIndex 基础索引（可选依赖）"""
from pathlib import Path

def mock_index(texts: list[str]) -> dict:
  # 无 llama-index 时的教学占位
  return {f"doc_{i}": t for i, t in enumerate(texts)}

def query(index: dict, q: str) -> str:
  for k, v in index.items():
    if any(c in v for c in q):
      return v
  return "未找到相关文档"

if __name__ == "__main__":
  idx = mock_index(["年假5天", "报销需发票"])
  print(query(idx, "年假"))
