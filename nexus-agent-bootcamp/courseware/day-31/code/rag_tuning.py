#!/usr/bin/env python3
"""Day 31: RAG 超参数网格搜索"""
from dataclasses import dataclass

@dataclass
class RagConfig:
  chunk_size: int
  top_k: int
  temperature: float

EVAL_QUERIES = [
  ("年假几天", "5"),
  ("报销要什么", "发票"),
]

def score_config(cfg: RagConfig) -> float:
  # 教学 mock：chunk 适中、top_k=3、temperature 低 得分高
  s = 0.0
  if 200 <= cfg.chunk_size <= 400: s += 0.4
  if cfg.top_k == 3: s += 0.3
  if cfg.temperature <= 0.3: s += 0.3
  return s

if __name__ == "__main__":
  best = max(
    [RagConfig(cs, k, t) for cs in [200, 300, 500] for k in [2, 3, 5] for t in [0.0, 0.3, 0.7]],
    key=score_config,
  )
  print("最佳配置:", best, "score=", score_config(best))
