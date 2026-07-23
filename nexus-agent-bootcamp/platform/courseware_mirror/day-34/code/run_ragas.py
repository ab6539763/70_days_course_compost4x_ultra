#!/usr/bin/env python3
"""Day 34: 批量评估脚本"""
import json
from pathlib import Path
from ragas_eval import RagSample, faithfulness, answer_relevancy

def run_eval() -> None:
  data = json.loads(Path("eval_dataset.json").read_text(encoding="utf-8"))
  for row in data:
    ans = row.get("predicted", row["ground_truth"])
    f = faithfulness(ans, row["contexts"])
    r = answer_relevancy(ans, row["question"])
    print(row["question"], f"F={f:.2f} R={r:.2f}")

if __name__ == "__main__":
  run_eval()
