#!/usr/bin/env python3
"""
Day 16 实操：大模型 API 参数实验
对比 temperature、top_p、max_tokens 对输出风格的影响。
支持 MOCK 模式（无 API Key 时自动启用）。
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

PROMPT = "用一句话介绍智链科技的 NexusAgent 平台。"


def call_chat(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 1.0,
    max_tokens: int = 256,
) -> str:
    """调用 Chat Completions API；无 Key 时返回模拟结果。"""
    if not API_KEY:
        return (
            f"[MOCK] temp={temperature} top_p={top_p} max_tokens={max_tokens} → "
            f"NexusAgent 是企业级多 Agent 协作平台，支持知识问答与工具调用。"
        )

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        f"{API_BASE}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
        return f"[ERROR] API 调用失败: {exc}"


def run_experiments() -> None:
    """依次测试不同参数组合。"""
    experiments = [
        {"temperature": 0.0, "top_p": 1.0, "max_tokens": 64, "label": "确定性（temp=0）"},
        {"temperature": 0.7, "top_p": 1.0, "max_tokens": 128, "label": "默认创意（temp=0.7）"},
        {"temperature": 1.2, "top_p": 1.0, "max_tokens": 128, "label": "高随机（temp=1.2）"},
        {"temperature": 0.7, "top_p": 0.3, "max_tokens": 128, "label": "核采样收紧（top_p=0.3）"},
        {"temperature": 0.7, "top_p": 1.0, "max_tokens": 20, "label": "截断（max_tokens=20）"},
    ]

    print("=" * 60)
    print("Day 16 — API 参数实验")
    print("=" * 60)
    print(f"Prompt: {PROMPT}\n")

    for exp in experiments:
        print(f"--- {exp['label']} ---")
        result = call_chat(
            PROMPT,
            temperature=exp["temperature"],
            top_p=exp["top_p"],
            max_tokens=exp["max_tokens"],
        )
        print(result)
        print()


if __name__ == "__main__":
    run_experiments()
