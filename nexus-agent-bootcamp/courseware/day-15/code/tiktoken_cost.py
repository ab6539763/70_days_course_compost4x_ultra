#!/usr/bin/env python3
"""
Day 15 实操：Token 计数与 API 费用估算
演示 tiktoken 分词原理，并估算不同模型的调用成本。
无 API Key 时可纯本地运行（仅做 token 统计）。
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class ModelPricing:
    """模型定价表（每百万 token，单位：人民币元，教学用近似值）。"""

    name: str
    input_per_million: float
    output_per_million: float


# 常见模型定价（教学演示，请以厂商官网为准）
PRICING_TABLE: list[ModelPricing] = [
    ModelPricing("deepseek-chat", 1.0, 2.0),
    ModelPricing("gpt-4o-mini", 1.1, 4.4),
    ModelPricing("qwen-plus", 0.8, 2.0),
]


def count_tokens_simple(text: str) -> int:
    """
    简易 token 估算：中文约 1.5 字/token，英文约 4 字符/token。
    生产环境请使用 tiktoken 或厂商 tokenizer。
    """
    chinese_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    other_chars = len(text) - chinese_chars
    return int(chinese_chars / 1.5 + other_chars / 4) + 1


def count_tokens_tiktoken(text: str, model: str = "cl100k_base") -> int | None:
    """使用 tiktoken 精确计数；未安装时返回 None。"""
    try:
        import tiktoken  # type: ignore

        try:
            enc = tiktoken.encoding_for_model(model)
        except KeyError:
            enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        return None


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    pricing: ModelPricing,
) -> dict[str, float]:
    """根据 token 数估算单次调用费用（元）。"""
    input_cost = input_tokens / 1_000_000 * pricing.input_per_million
    output_cost = output_tokens / 1_000_000 * pricing.output_per_million
    return {
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(input_cost + output_cost, 6),
    }


def demo_conversation_cost() -> None:
    """模拟一段多轮对话的 token 与费用。"""
    system_prompt = "你是智链科技 Nexus 项目的 AI 助手，回答简洁专业。"
    user_messages = [
        "什么是大语言模型？用三句话解释。",
        "它和传统搜索引擎有什么区别？",
        "我们项目里 Day 15 为什么要学 token 计数？",
    ]

    print("=" * 60)
    print("Day 15 — Token 计数与费用估算演示")
    print("=" * 60)

    total_input = count_tokens_tiktoken(system_prompt) or count_tokens_simple(system_prompt)
    print(f"\n[System] tokens ≈ {total_input}")

    for i, msg in enumerate(user_messages, 1):
        tokens = count_tokens_tiktoken(msg) or count_tokens_simple(msg)
        total_input += tokens
        # 假设模型回复约为用户输入的 2 倍 token
        assumed_reply_tokens = tokens * 2
        print(f"\n[User {i}] {msg[:40]}...")
        print(f"  用户 tokens ≈ {tokens}，假设回复 tokens ≈ {assumed_reply_tokens}")

    assumed_output = total_input  # 简化：输出总量约等于输入
    print(f"\n累计输入 tokens ≈ {total_input}")
    print(f"累计输出 tokens（估算）≈ {assumed_output}")

    print("\n--- 各模型费用估算（单次多轮对话）---")
    for p in PRICING_TABLE:
        cost = estimate_cost(total_input, assumed_output, p)
        print(
            f"  {p.name:20s}  输入 ¥{cost['input_cost']:.4f}  "
            f"输出 ¥{cost['output_cost']:.4f}  合计 ¥{cost['total_cost']:.4f}"
        )

    print("\n提示：设置环境变量 DEEPSEEK_API_KEY 后可对接真实 API 做对比验证。")
    if os.getenv("DEEPSEEK_API_KEY"):
        print("  检测到 DEEPSEEK_API_KEY，可在作业中扩展真实调用统计。")
    else:
        print("  当前为纯本地演示模式（无需 API Key）。")


if __name__ == "__main__":
    demo_conversation_cost()
