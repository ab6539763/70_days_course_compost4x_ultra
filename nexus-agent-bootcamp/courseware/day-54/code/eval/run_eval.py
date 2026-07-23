#!/usr/bin/env python3
"""
Day 54 — 微调模型评估
使用 ROUGE-L 与人工抽检清单评估领域问答质量
"""
from __future__ import annotations

import json
from pathlib import Path


def rouge_l_score(prediction: str, reference: str) -> float:
    """简化版 ROUGE-L F1（基于最长公共子序列）"""
    pred_tokens = prediction.split()
    ref_tokens = reference.split()
    if not pred_tokens or not ref_tokens:
        return 0.0

    m, n = len(pred_tokens), len(ref_tokens)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pred_tokens[i - 1] == ref_tokens[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[m][n]
    precision = lcs / m
    recall = lcs / n
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def evaluate_predictions(predictions: list[dict], threshold: float = 0.3) -> dict:
    """批量评估，返回统计摘要"""
    scores = [rouge_l_score(p["prediction"], p["reference"]) for p in predictions]
    passed = sum(1 for s in scores if s >= threshold)
    return {
        "total": len(scores),
        "avg_rouge_l": sum(scores) / len(scores),
        "pass_rate": passed / len(scores),
        "threshold": threshold,
    }


SAMPLE_EVAL = [
    {"prediction": "登录管理后台进入系统设置安全重置密码", "reference": "登录管理后台，进入系统设置安全重置密码"},
    {"prediction": "检查向量化状态和 Chroma 服务", "reference": "检查文档向量化状态与 Chroma 服务连通性"},
]


def main() -> None:
    result = evaluate_predictions(SAMPLE_EVAL)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
