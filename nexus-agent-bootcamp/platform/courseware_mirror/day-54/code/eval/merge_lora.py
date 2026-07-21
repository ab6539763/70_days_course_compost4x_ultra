#!/usr/bin/env python3
"""Day 54 — LoRA 权重合并脚本"""
from __future__ import annotations

import subprocess


def merge_lora(base_model: str, adapter_path: str, output_path: str, dry_run: bool = True) -> None:
    cmd = [
        "llamafactory-cli", "export",
        "--model_name_or_path", base_model,
        "--adapter_name_or_path", adapter_path,
        "--template", "qwen",
        "--finetuning_type", "lora",
        "--export_dir", output_path,
    ]
    print(" ".join(cmd))
    if not dry_run:
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    merge_lora("Qwen/Qwen2.5-7B-Instruct", "output/nexus-qwen-lora", "output/nexus-qwen-merged")
