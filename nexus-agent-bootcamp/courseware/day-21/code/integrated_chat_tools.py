#!/usr/bin/env python3
"""
Day 21 周测综合：集成对话 + 意图分类 + 工具调用 + FAQ 检索
模拟 NexusAgent v0.2 前的核心推理链路（单文件可运行）。
"""
from __future__ import annotations

import json
import math
import os
import re
import urllib.error
import urllib.request
from typing import Any

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

FAQ = [
    "NexusAgent 是企业级智能体平台",
    "支持 RAG 知识库与多 Agent 编排",
    "第二阶段将交付 Web 聊天界面",
]

INTENTS = ["查天气", "做计算", "查FAQ", "闲聊"]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[\u4e00-\u9fff]|[a-zA-Z0-9]+", text)


def faq_search(query: str) -> str:
    """简易 FAQ 检索。"""
    q_tokens = set(tokenize(query.lower()))
    best, best_score = FAQ[0], 0.0
    for doc in FAQ:
        d_tokens = set(tokenize(doc.lower()))
        inter = len(q_tokens & d_tokens)
        score = inter / max(len(q_tokens | d_tokens), 1)
        if score > best_score:
            best_score, best = score, doc
    return best


def get_weather(city: str) -> str:
    return json.dumps({"city": city, "temp": 26, "condition": "晴"}, ensure_ascii=False)


def calculate(expr: str) -> str:
    try:
        result = eval(expr, {"__builtins__": {}}, {"sqrt": math.sqrt})  # noqa: S307
        return str(result)
    except Exception as exc:  # noqa: BLE001
        return f"计算错误: {exc}"


def classify_intent(text: str) -> str:
    """规则意图分类（周测综合演示）。"""
    if "天气" in text:
        return "查天气"
    if re.search(r"[\d+\-*/]", text) or "计算" in text or "算" in text:
        return "做计算"
    if any(k in text for k in ["Nexus", "平台", "RAG", "Agent", "什么"]):
        return "查FAQ"
    return "闲聊"


def chat_llm(prompt: str) -> str:
    if not API_KEY:
        return f"【MOCK 闲聊回复】收到：{prompt[:50]}"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
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
        return data["choices"][0]["message"]["content"].strip()
    except urllib.error.URLError as exc:
        return f"API 错误: {exc}"


def handle_message(user_input: str) -> str:
    """统一消息处理入口。"""
    intent = classify_intent(user_input)
    print(f"  [意图] {intent}")

    if intent == "查天气":
        city = "北京" if "北京" in user_input else "上海"
        return f"天气信息: {get_weather(city)}"
    if intent == "做计算":
        expr = re.search(r"[\d.+*/()-sqrt]+", user_input.replace(" ", ""))
        if expr:
            return f"结果: {calculate(expr.group())}"
        return "请提供数学表达式"
    if intent == "查FAQ":
        return f"FAQ 命中: {faq_search(user_input)}"
    return chat_llm(user_input)


def repl() -> None:
    """交互式 REPL。"""
    print("=" * 60)
    print("Day 21 — 周测综合助手（输入 quit 退出）")
    print("=" * 60)
    print("试试: 北京天气 / 计算 2**10 / NexusAgent 是什么 / 你好")

    while True:
        try:
            user_input = input("\n你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break
        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "q"}:
            print("再见！")
            break
        reply = handle_message(user_input)
        print(f"助手: {reply}")


if __name__ == "__main__":
    repl()
