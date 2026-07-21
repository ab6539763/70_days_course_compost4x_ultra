#!/usr/bin/env python3
"""
Day 17 实操：Prompt 模板库（10 个企业场景）
每个场景包含 system / user 模板与变量占位符，可直接填充后调用 API。
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# 10 个场景模板：键为场景名，值为 system + user 模板
PROMPT_SCENARIOS: dict[str, dict[str, str]] = {
    "翻译": {
        "system": "你是专业翻译，保留术语准确性，输出仅含译文。",
        "user": "将以下{source_lang}文本翻译为{target_lang}：\n{text}",
    },
    "摘要": {
        "system": "你是企业文档分析师，输出结构化摘要：背景、要点、行动项。",
        "user": "请摘要以下会议纪要（不超过{max_words}字）：\n{content}",
    },
    "代码解释": {
        "system": "你是资深 Python 工程师，用初学者能懂的语言解释代码。",
        "user": "解释以下代码的功能与潜在问题：\n```python\n{code}\n```",
    },
    "邮件撰写": {
        "system": "你是商务沟通专家，语气{tone}，格式规范。",
        "user": "给{recipient}写一封关于{topic}的邮件，要点：{points}",
    },
    "角色扮演": {
        "system": "你扮演{role}，回答需符合该角色专业知识与口吻。",
        "user": "{question}",
    },
    "数据分析": {
        "system": "你是数据分析师，给出洞察与可视化建议，不编造数据。",
        "user": "数据集描述：{dataset_desc}\n问题：{question}",
    },
    "头脑风暴": {
        "system": "你是产品创新顾问，输出{count}个可执行创意，编号列出。",
        "user": "为{product}在{scenario}场景头脑风暴新功能。",
    },
    "纠错": {
        "system": "你是文字编辑，修正语法与逻辑错误，并说明修改理由。",
        "user": "请纠错：\n{text}",
    },
    "格式转换": {
        "system": "你是格式转换工具，严格按目标格式输出，不加多余说明。",
        "user": "将以下{source_format}转为{target_format}：\n{content}",
    },
    "教学辅导": {
        "system": "你是耐心导师，用例子与类比讲解，最后出一道练习题。",
        "user": "学员水平：{level}。请教我：{topic}",
    },
}


def fill_template(template: str, variables: dict[str, Any]) -> str:
    """安全填充模板变量。"""
    return template.format(**variables)


def build_messages(scenario: str, variables: dict[str, Any]) -> list[dict[str, str]]:
    """根据场景名与变量构建 messages 列表。"""
    if scenario not in PROMPT_SCENARIOS:
        raise ValueError(f"未知场景: {scenario}，可选: {list(PROMPT_SCENARIOS)}")
    tpl = PROMPT_SCENARIOS[scenario]
    return [
        {"role": "system", "content": fill_template(tpl["system"], variables)},
        {"role": "user", "content": fill_template(tpl["user"], variables)},
    ]


def call_llm(messages: list[dict[str, str]]) -> str:
    """调用大模型；无 Key 时返回 MOCK 摘要。"""
    user_preview = messages[-1]["content"][:80].replace("\n", " ")
    if not API_KEY:
        return f"[MOCK/{messages[0]['content'][:12]}...] 已收到: {user_preview}..."

    payload = {"model": MODEL, "messages": messages, "temperature": 0.7}
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
    except (urllib.error.URLError, KeyError) as exc:
        return f"[ERROR] {exc}"


# 每个场景的演示变量
DEMO_VARIABLES: dict[str, dict[str, Any]] = {
    "翻译": {"source_lang": "中文", "target_lang": "英文", "text": "智链科技推出 NexusAgent 智能体平台。"},
    "摘要": {"max_words": "150", "content": "周会讨论 Q2 上线 Web 聊天与 RAG 排期，陈工负责架构评审。"},
    "代码解释": {"code": "def add(a, b):\n    return a + b"},
    "邮件撰写": {"tone": "正式", "recipient": "客户张总", "topic": "项目进度", "points": "已完成 API 联调"},
    "角色扮演": {"role": "数据库 DBA", "question": "SQLite 和 PostgreSQL 怎么选型？"},
    "数据分析": {"dataset_desc": "销售 CSV，字段：日期/区域/金额", "question": "哪个区域增长最快？"},
    "头脑风暴": {"count": "5", "product": "NexusAgent", "scenario": "客服"},
    "纠错": {"text": "我们公司昨天开会讨论了关于AI的项目，效果还不错。"},
    "格式转换": {"source_format": "JSON", "target_format": "Markdown 表格", "content": '{"name":"Nexus","version":1}'},
    "教学辅导": {"level": "零基础", "topic": "什么是 Prompt？"},
}


def run_all_scenarios() -> None:
    """依次运行 10 个场景演示。"""
    print("=" * 60)
    print("Day 17 — Prompt 模板库（10 场景）")
    print("=" * 60)
    for i, name in enumerate(PROMPT_SCENARIOS, 1):
        print(f"\n[{i}/10] 场景：{name}")
        messages = build_messages(name, DEMO_VARIABLES[name])
        print(f"  System: {messages[0]['content'][:50]}...")
        result = call_llm(messages)
        print(f"  输出: {result[:200]}{'...' if len(result) > 200 else ''}")


if __name__ == "__main__":
    run_all_scenarios()
