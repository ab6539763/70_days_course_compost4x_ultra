#!/usr/bin/env python3
"""
Day 18 实操：意图分类器（JSON 结构化输出）
将用户输入分类为预定义意图，强制模型返回可解析 JSON。
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# 智链客服场景意图标签
INTENTS = [
    "查询订单",
    "退换货",
    "产品咨询",
    "技术支持",
    "投诉建议",
    "闲聊",
]

SYSTEM_PROMPT = f"""你是智链科技客服意图分类器。
请将用户消息分类为以下意图之一：{", ".join(INTENTS)}。
必须仅输出 JSON，格式：
{{"intent": "意图名", "confidence": 0.0-1.0, "entities": {{"key": "value"}}, "reason": "一句话理由"}}
不要输出 markdown 代码块或其他文字。"""


def extract_json(text: str) -> dict[str, Any]:
    """从模型回复中提取 JSON（兼容多余前后缀）。"""
    text = text.strip()
    # 去除 ```json ... ``` 包裹
    if "```" in text:
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            text = match.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        text = text[start : end + 1]
    return json.loads(text)


def mock_classify(user_text: str) -> dict[str, Any]:
    """规则 MOCK 分类，便于无 API 时演示。"""
    rules = [
        ("订单", "查询订单"),
        ("退货", "退换货"),
        ("换货", "退换货"),
        ("价格", "产品咨询"),
        ("功能", "产品咨询"),
        ("报错", "技术支持"),
        ("bug", "技术支持"),
        ("投诉", "投诉建议"),
    ]
    intent = "闲聊"
    for kw, label in rules:
        if kw in user_text:
            intent = label
            break
    return {
        "intent": intent,
        "confidence": 0.85 if intent != "闲聊" else 0.6,
        "entities": {},
        "reason": f"MOCK 规则匹配: {user_text[:20]}",
    }


def classify_intent(user_text: str) -> dict[str, Any]:
    """调用 LLM 进行意图分类，返回解析后的 dict。"""
    if not API_KEY:
        return mock_classify(user_text)

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
    }
    req = urllib.request.Request(
        f"{API_BASE}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        raw = data["choices"][0]["message"]["content"]
        return extract_json(raw)
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as exc:
        return {"intent": "未知", "confidence": 0.0, "entities": {}, "reason": str(exc)}


def demo() -> None:
    samples = [
        "帮我查一下订单 20240315001 的物流",
        "这个产品支持私有化部署吗？多少钱？",
        "上传文档后一直转圈，是不是坏了？",
        "你们客服态度太差了，我要投诉！",
        "今天天气不错啊",
    ]
    print("=" * 60)
    print("Day 18 — 意图分类器（JSON 输出）")
    print("=" * 60)
    for text in samples:
        result = classify_intent(text)
        print(f"\n用户: {text}")
        print(f"分类: {json.dumps(result, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    demo()
