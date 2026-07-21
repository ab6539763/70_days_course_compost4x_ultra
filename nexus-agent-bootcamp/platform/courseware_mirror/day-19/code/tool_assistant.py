#!/usr/bin/env python3
"""
Day 19 实操：Function Calling 工具助手（无框架）
手写工具注册、参数解析与多轮 tool_calls 循环。
内置工具：get_weather（模拟）、calculate（安全 eval）。
"""
from __future__ import annotations

import json
import math
import os
import re
import urllib.error
import urllib.request
from typing import Any, Callable

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# ---------- 工具实现 ----------


def get_weather(city: str) -> dict[str, Any]:
    """模拟天气查询（教学用固定数据）。"""
    db = {
        "北京": {"temp": 28, "condition": "晴", "humidity": 35},
        "上海": {"temp": 32, "condition": "多云", "humidity": 70},
        "深圳": {"temp": 30, "condition": "阵雨", "humidity": 80},
    }
    info = db.get(city, {"temp": 25, "condition": "未知", "humidity": 50})
    return {"city": city, **info, "source": "mock_weather_api"}


def calculate(expression: str) -> dict[str, Any]:
    """
    安全计算数学表达式。
    仅允许数字、运算符与 math 模块常用函数。
    """
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    allowed_names.update({"abs": abs, "round": round})
    # 白名单字符检查
    if not re.match(r"^[\d\s+\-*/().,a-zA-Z_]+$", expression):
        return {"error": "表达式含非法字符", "expression": expression}
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307
        return {"expression": expression, "result": result}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc), "expression": expression}


# 工具 JSON Schema（OpenAI 兼容格式）
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名，如北京"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式，支持 sqrt、sin 等",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式，如 2**10 + sqrt(16)"}
                },
                "required": ["expression"],
            },
        },
    },
]

TOOL_REGISTRY: dict[str, Callable[..., dict[str, Any]]] = {
    "get_weather": get_weather,
    "calculate": calculate,
}


def dispatch_tool(name: str, arguments: dict[str, Any]) -> str:
    """根据工具名调用并返回 JSON 字符串。"""
    fn = TOOL_REGISTRY.get(name)
    if not fn:
        return json.dumps({"error": f"未知工具: {name}"}, ensure_ascii=False)
    return json.dumps(fn(**arguments), ensure_ascii=False)


def mock_agent(user_query: str) -> str:
    """无 API 时的规则路由演示。"""
    if "天气" in user_query:
        city = "北京" if "北京" in user_query else "上海"
        return f"{city}天气：{json.dumps(get_weather(city), ensure_ascii=False)}"
    if any(op in user_query for op in ["计算", "+", "*", "sqrt"]):
        expr = re.search(r"[\d.+*/()-]+", user_query)
        if expr:
            return f"计算结果：{json.dumps(calculate(expr.group()), ensure_ascii=False)}"
    return "【MOCK】我可以查天气或做计算，请明确您的需求。"


def run_tool_loop(user_query: str, max_rounds: int = 5) -> str:
    """多轮 tool_calls 循环直至模型给出最终回复。"""
    if not API_KEY:
        return mock_agent(user_query)

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": "你是 Nexus 助手，可调用工具回答问题。"},
        {"role": "user", "content": user_query},
    ]

    for _ in range(max_rounds):
        payload = {"model": MODEL, "messages": messages, "tools": TOOLS, "tool_choice": "auto"}
        req = urllib.request.Request(
            f"{API_BASE}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        msg = data["choices"][0]["message"]
        messages.append(msg)

        tool_calls = msg.get("tool_calls")
        if not tool_calls:
            return msg.get("content", "")

        for tc in tool_calls:
            fn = tc["function"]
            args = json.loads(fn["arguments"])
            result = dispatch_tool(fn["name"], args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": result,
                }
            )

    return "超过最大工具调用轮次。"


def main() -> None:
    queries = [
        "北京今天天气怎么样？",
        "帮我算一下 sqrt(144) + 2**10",
    ]
    print("=" * 60)
    print("Day 19 — Function Calling 工具助手")
    print("=" * 60)
    for q in queries:
        print(f"\n用户: {q}")
        print(f"助手: {run_tool_loop(q)}")


if __name__ == "__main__":
    main()
