#!/bin/bash
# Day 53 — 启动 LLaMA-Factory 微调（需提前安装 llamafactory）
set -euo pipefail

echo "=== NexusAgent 微调训练启动 ==="
export CUDA_VISIBLE_DEVICES=0

# 检查数据文件
if [ ! -f "../dataset/data/nexus_qa_train.json" ]; then
  echo "请先运行 dataset/prepare_dataset.py 生成训练数据"
  exit 1
fi

llamafactory-cli train train_config.yaml

echo "训练完成，LoRA 权重保存在 output/nexus-qwen-lora/"
