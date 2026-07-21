#!/usr/bin/env python3
"""数据集质量报告：统计 token 长度分布、重复率"""
import json
from collections import Counter
from pathlib import Path


def analyze_dataset(path: Path) -> None:
    records = json.loads(path.read_text(encoding="utf-8"))
    lengths = [len(r["instruction"]) + len(r.get("input", "")) + len(r["output"]) for r in records]
    outputs = [r["output"] for r in records]
    dup_rate = 1 - len(set(outputs)) / max(len(outputs), 1)

    print(f"样本总数: {len(records)}")
    print(f"平均字符长度: {sum(lengths)/len(lengths):.0f}")
    print(f"最短/最长: {min(lengths)} / {max(lengths)}")
    print(f"输出重复率: {dup_rate:.1%}")
    if dup_rate > 0.1:
        print("⚠️  重复率偏高，建议去重或增广数据")


if __name__ == "__main__":
    analyze_dataset(Path("data/nexus_qa_train.json"))
