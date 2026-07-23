#!/usr/bin/env python3
"""
Day 51 — 微调理论：LoRA 低秩分解参数量估算
演示为何 LoRA 能以极少参数实现高效微调
"""
from __future__ import annotations


def lora_param_count(
    in_features: int,
    out_features: int,
    rank: int,
    num_layers: int = 1,
) -> int:
    """
    计算 LoRA 可训练参数量
    每层 LoRA: A(in×r) + B(r×out) = r*(in+out)
    """
    per_layer = rank * (in_features + out_features)
    return per_layer * num_layers


def full_finetune_param_count(num_params_billion: float) -> int:
    """全量微调参数量（单位：个）"""
    return int(num_params_billion * 1e9)


def main() -> None:
    # 以 7B 模型 hidden=4096, 32 层 attention 为例
    hidden = 4096
    layers = 32
    rank = 8

    lora_params = lora_param_count(hidden, hidden, rank, layers * 4)  # Q/K/V/O
    full_params = full_finetune_param_count(7.0)

    ratio = lora_params / full_params * 100
    print(f"全量微调参数量: {full_params:,}")
    print(f"LoRA(r={rank}) 可训练参数: {lora_params:,}")
    print(f"LoRA 占比: {ratio:.4f}%")
    print("\n结论: LoRA 将显存与存储需求降低 2-3 个数量级，适合企业领域适配。")


if __name__ == "__main__":
    main()
