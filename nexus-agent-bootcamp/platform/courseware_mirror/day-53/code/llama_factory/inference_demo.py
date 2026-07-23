#!/usr/bin/env python3
"""
Day 53 — 微调后推理演示（Mock 模式，无 GPU 亦可运行）
真实环境请替换为 llamafactory-cli chat 或 vLLM 加载
"""
from __future__ import annotations


def mock_inference(prompt: str, lora_path: str = "output/nexus-qwen-lora") -> str:
    """模拟 LoRA 模型推理，教学环境无显卡时使用"""
    # 生产环境: 加载 base_model + lora_adapter
    responses = {
        "重置密码": "请登录管理后台，进入「系统设置 > 安全」完成重置。",
        "RAG": "请检查文档向量化状态与 Chroma 服务连通性。",
    }
    for key, resp in responses.items():
        if key in prompt:
            return f"[LoRA@{lora_path}] {resp}"
    return f"[LoRA@{lora_path}] 我是 NexusAgent 领域助手，请问有什么可以帮您？"


def main() -> None:
    test_prompts = [
        "如何重置 NexusAgent 管理员密码？",
        "RAG 检索结果为空怎么办？",
        "你好",
    ]
    for p in test_prompts:
        print(f"Q: {p}")
        print(f"A: {mock_inference(p)}\n")


if __name__ == "__main__":
    main()
