#!/usr/bin/env python3
"""对比不同微调策略的配置差异（教学演示，非真实训练）"""
from dataclasses import dataclass


@dataclass
class FinetuneConfig:
    method: str
    base_model: str
    trainable_ratio: str
    min_vram_gb: int
    recommended_dataset_size: str


PRESETS = [
    FinetuneConfig("Full FT", "Qwen2.5-7B", "100%", 80, "10万+"),
    FinetuneConfig("LoRA", "Qwen2.5-7B", "~0.5%", 24, "5000+"),
    FinetuneConfig("QLoRA", "Qwen2.5-7B", "~0.5%", 16, "3000+"),
]


def print_comparison() -> None:
    print(f"{'方法':<10} {'基座':<14} {'可训练':<8} {'最低显存':<10} {'数据量'}")
    print("-" * 60)
    for p in PRESETS:
        print(f"{p.method:<10} {p.base_model:<14} {p.trainable_ratio:<8} {p.min_vram_gb}GB{'':<6} {p.recommended_dataset_size}")


if __name__ == "__main__":
    print_comparison()
