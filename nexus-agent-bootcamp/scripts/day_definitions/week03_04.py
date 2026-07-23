"""
NexusAgent 训练营 Day 15-24 课件定义
Phase 2：大模型基础与Prompt工程 | Epic NEXUS-E2
"""
from __future__ import annotations

import sys
from pathlib import Path

# 确保可从 scripts/ 目录导入 generate_courseware
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from generate_courseware import DayPlan  # noqa: E402

PHASE_2 = "Phase 2：大模型基础与Prompt工程"
EPIC_E2 = "NEXUS-E2"


def _jira(day: int, *suffixes: str) -> list[str]:
    """生成当日 Jira Story 编号，如 NEXUS-215-1。"""
    return [f"NEXUS-{day}{s}" for s in suffixes]


# ---------------------------------------------------------------------------
# Day 15 代码：tiktoken_cost.py
# ---------------------------------------------------------------------------
TIKTOKEN_COST_PY = r'''#!/usr/bin/env python3
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
'''

# ---------------------------------------------------------------------------
# Day 16 代码
# ---------------------------------------------------------------------------
PARAM_EXPERIMENT_PY = r'''#!/usr/bin/env python3
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
'''

STREAM_OUTPUT_PY = r'''#!/usr/bin/env python3
"""
Day 16 实操：流式输出（Streaming）
演示 SSE 风格逐 token 打印，模拟 ChatGPT 打字机效果。
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")


def mock_stream(text: str, delay: float = 0.03) -> None:
    """无 API 时的模拟流式输出。"""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def stream_chat(prompt: str) -> None:
    """流式调用 Chat API 并实时打印。"""
    if not API_KEY:
        mock_stream(
            "【MOCK 流式】NexusAgent 平台通过 REST API 与 SSE "
            "为前端提供实时对话能力，是 Day 22-24 的前置基础。"
        )
        return

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "temperature": 0.7,
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

    print("助手: ", end="", flush=True)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8").strip()
                if not line or not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        sys.stdout.write(content)
                        sys.stdout.flush()
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
        print()
    except urllib.error.URLError as exc:
        print(f"\n[ERROR] 流式请求失败: {exc}")


def main() -> None:
    prompt = "用三句话解释什么是 Server-Sent Events（SSE）。"
    print("=" * 60)
    print("Day 16 — 流式输出演示")
    print("=" * 60)
    print(f"用户: {prompt}\n")
    stream_chat(prompt)


if __name__ == "__main__":
    main()
'''

# ---------------------------------------------------------------------------
# Day 17 代码：prompt_templates.py（10 场景）
# ---------------------------------------------------------------------------
PROMPT_TEMPLATES_PY = r'''#!/usr/bin/env python3
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
'''

# ---------------------------------------------------------------------------
# Day 18 代码：intent_classifier.py
# ---------------------------------------------------------------------------
INTENT_CLASSIFIER_PY = r'''#!/usr/bin/env python3
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
'''

# ---------------------------------------------------------------------------
# Day 19 代码：tool_assistant.py
# ---------------------------------------------------------------------------
TOOL_ASSISTANT_PY = r'''#!/usr/bin/env python3
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
'''

# ---------------------------------------------------------------------------
# Day 20 代码：similarity_matcher.py
# ---------------------------------------------------------------------------
SIMILARITY_MATCHER_PY = r'''#!/usr/bin/env python3
"""
Day 20 实操：文本 Embedding 与语义相似度匹配
演示向量表示、余弦相似度，以及简单 FAQ 检索。
无 API 时使用 TF-IDF 风格词袋向量作为 fallback。
"""
from __future__ import annotations

import json
import math
import os
import re
import urllib.error
import urllib.request
from collections import Counter
from typing import Any

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

FAQ_CORPUS = [
    {"id": "faq-01", "question": "NexusAgent 支持哪些大模型？", "answer": "支持 DeepSeek、Qwen、OpenAI 兼容 API。"},
    {"id": "faq-02", "question": "如何上传企业知识库文档？", "answer": "Day 25 起支持 PDF/Word 上传并向量化。"},
    {"id": "faq-03", "question": "是否支持私有化部署？", "answer": "支持 Docker 私有化，Day 56 详解。"},
    {"id": "faq-04", "question": "API 调用如何计费？", "answer": "按 token 计费，可在控制台查看用量。"},
    {"id": "faq-05", "question": "能否对接飞书机器人？", "answer": "Day 45 将讲解 Webhook 与飞书集成。"},
]


def tokenize(text: str) -> list[str]:
    """简单分词：中文按字、英文按单词。"""
    chars = re.findall(r"[\u4e00-\u9fff]", text)
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return chars + words


def bag_of_words_vector(text: str, vocab: dict[str, int]) -> list[float]:
    """词袋向量（教学 fallback）。"""
    counts = Counter(tokenize(text))
    return [float(counts.get(w, 0)) for w in vocab]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算余弦相似度。"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def build_vocab(texts: list[str]) -> dict[str, int]:
    """构建词表。"""
    vocab: dict[str, int] = {}
    for t in texts:
        for tok in set(tokenize(t)):
            if tok not in vocab:
                vocab[tok] = len(vocab)
    return vocab


def get_embedding_api(text: str) -> list[float] | None:
    """调用 Embedding API；失败返回 None。"""
    if not API_KEY:
        return None
    payload = {"model": EMBED_MODEL, "input": text}
    req = urllib.request.Request(
        f"{API_BASE}/v1/embeddings",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["data"][0]["embedding"]
    except (urllib.error.URLError, KeyError, json.JSONDecodeError):
        return None


def embed_texts(texts: list[str]) -> list[list[float]]:
    """批量向量化；优先 API，否则词袋。"""
    api_vecs = [get_embedding_api(t) for t in texts]
    if all(v is not None for v in api_vecs):
        return api_vecs  # type: ignore[list-item]

    print("  [INFO] 使用本地词袋向量（未配置 API 或 Embedding 不可用）")
    vocab = build_vocab(texts)
    return [bag_of_words_vector(t, vocab) for t in texts]


def search_faq(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """语义检索 FAQ，返回 top_k 条。"""
    questions = [item["question"] for item in FAQ_CORPUS]
    all_texts = questions + [query]
    vectors = embed_texts(all_texts)
    query_vec = vectors[-1]
    doc_vecs = vectors[:-1]

    scored = []
    for item, vec in zip(FAQ_CORPUS, doc_vecs):
        score = cosine_similarity(query_vec, vec)
        scored.append({**item, "score": round(score, 4)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def main() -> None:
    queries = [
        "你们平台能接什么模型？",
        "怎么把公司文档放进去？",
        "本地服务器能装吗？",
    ]
    print("=" * 60)
    print("Day 20 — Embedding 语义相似度匹配")
    print("=" * 60)
    for q in queries:
        print(f"\n查询: {q}")
        results = search_faq(q)
        for r in results:
            print(f"  [{r['score']:.4f}] {r['question']}")
            print(f"         → {r['answer']}")


if __name__ == "__main__":
    main()
'''

# ---------------------------------------------------------------------------
# Day 21 代码：integrated_chat_tools.py
# ---------------------------------------------------------------------------
INTEGRATED_CHAT_TOOLS_PY = r'''#!/usr/bin/env python3
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
'''

# ---------------------------------------------------------------------------
# Day 22 前端代码
# ---------------------------------------------------------------------------
FRONTEND_INDEX_HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>NexusAgent 聊天 — Day 22</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <div class="app">
    <header class="header">
      <h1>🤖 NexusAgent</h1>
      <p class="subtitle">智链科技 · Day 22 静态聊天原型</p>
    </header>
    <main id="chat-window" class="chat-window" aria-live="polite">
      <div class="message bot">
        <div class="bubble">你好！我是 Nexus 助手，有什么可以帮你？</div>
      </div>
    </main>
    <footer class="input-area">
      <input id="user-input" type="text" placeholder="输入消息，按 Enter 发送..." autocomplete="off" />
      <button id="send-btn" type="button">发送</button>
    </footer>
  </div>
  <script src="chat.js"></script>
</body>
</html>
'''

FRONTEND_STYLE_CSS = r'''/* Day 22 — NexusAgent 聊天界面样式 */
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  min-height: 100vh; color: #e2e8f0;
}
.app { max-width: 720px; margin: 0 auto; height: 100vh; display: flex; flex-direction: column; padding: 16px; }
.header { text-align: center; padding: 12px 0 20px; }
.header h1 { font-size: 1.5rem; }
.subtitle { font-size: 0.85rem; color: #94a3b8; margin-top: 4px; }
.chat-window {
  flex: 1; overflow-y: auto; padding: 12px;
  background: rgba(15, 23, 42, 0.6); border-radius: 12px; border: 1px solid #334155;
}
.message { display: flex; margin-bottom: 12px; }
.message.user { justify-content: flex-end; }
.message.bot { justify-content: flex-start; }
.bubble {
  max-width: 80%; padding: 10px 14px; border-radius: 16px;
  line-height: 1.5; font-size: 0.95rem; white-space: pre-wrap; word-break: break-word;
}
.user .bubble { background: #3b82f6; color: #fff; border-bottom-right-radius: 4px; }
.bot .bubble { background: #334155; color: #f1f5f9; border-bottom-left-radius: 4px; }
.input-area { display: flex; gap: 8px; margin-top: 12px; }
#user-input {
  flex: 1; padding: 12px 16px; border-radius: 24px; border: 1px solid #475569;
  background: #1e293b; color: #f8fafc; font-size: 1rem; outline: none;
}
#user-input:focus { border-color: #3b82f6; }
#send-btn {
  padding: 12px 24px; border: none; border-radius: 24px;
  background: #3b82f6; color: #fff; font-size: 1rem; cursor: pointer;
}
#send-btn:hover { background: #2563eb; }
#send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.typing::after { content: "▋"; animation: blink 0.8s infinite; }
@keyframes blink { 50% { opacity: 0; } }
'''

FRONTEND_CHAT_JS = r'''/**
 * Day 22 — 静态聊天前端（MOCK 模式）
 * Day 23+ 将把 API_BASE 指向 FastAPI 后端。
 */
const API_BASE = window.NEXUS_API_BASE || "";

const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  div.appendChild(bubble);
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return bubble;
}

function mockReply(text) {
  if (text.includes("天气")) return "【MOCK】北京晴，26°C。";
  if (/[\d+\-*/]/.test(text)) return "【MOCK】计算功能将在后端接入。";
  if (text.includes("Nexus") || text.includes("平台"))
    return "【MOCK】NexusAgent 是智链科技的企业级智能体协作平台。";
  return `【MOCK】收到：「${text}」。Day 23 将对接真实 API。`;
}

async function fetchReply(text) {
  if (!API_BASE) return mockReply(text);
  const resp = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text }),
  });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  const data = await resp.json();
  return data.reply || data.content || "（空回复）";
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;
  userInput.value = "";
  sendBtn.disabled = true;
  appendMessage("user", text);
  const botBubble = appendMessage("bot", "");
  botBubble.classList.add("typing");
  try {
    const reply = await fetchReply(text);
    botBubble.classList.remove("typing");
    botBubble.textContent = reply;
  } catch (err) {
    botBubble.classList.remove("typing");
    botBubble.textContent = `请求失败: ${err.message}`;
  } finally {
    sendBtn.disabled = false;
    userInput.focus();
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});
userInput.focus();
'''

CHAT_API_PY = r'''#!/usr/bin/env python3
"""
Day 23 实操：FastAPI 聊天 API（上半）
提供 REST 端点 /api/chat，支持 CORS，可对接 Day 22 前端。
运行: uvicorn api.chat_api:app --reload --port 8000
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

app = FastAPI(title="NexusAgent Chat API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str | None = None
    model: str = MODEL


def call_llm(prompt: str) -> str:
    if not API_KEY:
        return f"【MOCK FastAPI】已收到: {prompt[:100]}"
    payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
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
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
        return f"LLM 调用失败: {exc}"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "nexus-chat-api"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    reply = call_llm(req.message)
    return ChatResponse(reply=reply, session_id=req.session_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.chat_api:app", host="0.0.0.0", port=8000, reload=True)
'''

DAY24_DATABASE_PY = r'''"""
Day 24 数据库层：SQLite 会话与消息持久化。
"""
from __future__ import annotations

import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "nexus_chat.db"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def get_conn() -> Generator[sqlite3.Connection, None, None]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY, title TEXT NOT NULL DEFAULT '新对话',
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL,
                role TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            );
            CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
        """)


def create_session(title: str = "新对话") -> str:
    session_id = str(uuid.uuid4())
    now = _utc_now()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO sessions (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (session_id, title, now, now),
        )
    return session_id


def add_message(session_id: str, role: str, content: str) -> int:
    now = _utc_now()
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (session_id, role, content, now),
        )
        conn.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (now, session_id))
        return int(cur.lastrowid)


def get_messages(session_id: str, limit: int = 50) -> list[dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT role, content, created_at FROM messages WHERE session_id = ? ORDER BY id ASC LIMIT ?",
            (session_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def list_sessions(limit: int = 20) -> list[dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title, created_at, updated_at FROM sessions ORDER BY updated_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]
'''

DAY24_MAIN_PY = r'''#!/usr/bin/env python3
"""
Day 24 实操：FastAPI 完整 Web Chat（下半）
特性：SSE 流式输出、SQLite 会话持久化、静态前端托管。
运行: python -m api.main  或  python api/main.py
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from api.database import add_message, create_session, get_messages, init_db, list_sessions

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend"

app = FastAPI(title="NexusAgent Web Chat", version="0.2.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str | None = None
    stream: bool = False


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.2.1"}


@app.get("/api/sessions")
def api_list_sessions() -> list[dict]:
    return list_sessions()


@app.get("/api/sessions/{session_id}/messages")
def api_get_messages(session_id: str) -> list[dict]:
    return get_messages(session_id)


def _build_llm_messages(session_id: str, user_msg: str) -> list[dict[str, str]]:
    history = get_messages(session_id, limit=20)
    messages = [{"role": "system", "content": "你是智链科技 NexusAgent 助手，回答简洁专业。"}]
    for m in history:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": user_msg})
    return messages


def _stream_llm(messages: list[dict[str, str]]) -> list[str]:
    if not API_KEY:
        return list(f"【MOCK SSE】{messages[-1]['content'][:80]} 的回复已写入数据库。")
    payload = {"model": MODEL, "messages": messages, "stream": True, "temperature": 0.7}
    req = urllib.request.Request(
        f"{API_BASE}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method="POST",
    )
    tokens: list[str] = []
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8").strip()
                if not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str == "[DONE]":
                    break
                chunk = json.loads(data_str)
                content = chunk["choices"][0].get("delta", {}).get("content", "")
                if content:
                    tokens.append(content)
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as exc:
        tokens = [f"流式调用失败: {exc}"]
    return tokens


async def sse_generator(session_id: str, user_msg: str) -> AsyncGenerator[str, None]:
    add_message(session_id, "user", user_msg)
    messages = _build_llm_messages(session_id, user_msg)
    messages = messages[:-1]
    messages.append({"role": "user", "content": user_msg})

    full_reply: list[str] = []
    for token in _stream_llm(messages):
        full_reply.append(token)
        payload = json.dumps({"token": token, "session_id": session_id}, ensure_ascii=False)
        yield f"data: {payload}\n\n"
        time.sleep(0.01)

    reply_text = "".join(full_reply)
    add_message(session_id, "assistant", reply_text)
    yield f"data: {json.dumps({'done': True, 'reply': reply_text}, ensure_ascii=False)}\n\n"


@app.post("/api/chat")
async def api_chat(req: ChatRequest) -> StreamingResponse | dict:
    session_id = req.session_id or create_session(title=req.message[:20])
    if req.stream:
        return StreamingResponse(
            sse_generator(session_id, req.message),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
    add_message(session_id, "user", req.message)
    tokens = _stream_llm(_build_llm_messages(session_id, req.message))
    reply = "".join(tokens)
    add_message(session_id, "assistant", reply)
    return {"reply": reply, "session_id": session_id}


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    print("启动 NexusAgent Web Chat → http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

DAY24_FRONTEND_CHAT_JS = r'''/**
 * Day 24 — 对接 SSE 流式 API 的前端增强版
 */
const API_BASE = window.NEXUS_API_BASE || "";
const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
let sessionId = localStorage.getItem("nexus_session_id") || null;

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  div.appendChild(bubble);
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return bubble;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;
  userInput.value = "";
  sendBtn.disabled = true;
  appendMessage("user", text);
  const botBubble = appendMessage("bot", "");
  botBubble.classList.add("typing");
  try {
    const resp = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: sessionId, stream: true }),
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    botBubble.textContent = "";
    botBubble.classList.remove("typing");
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";
      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const data = JSON.parse(line.slice(6));
        if (data.token) {
          botBubble.textContent += data.token;
          chatWindow.scrollTop = chatWindow.scrollHeight;
        }
        if (data.session_id) {
          sessionId = data.session_id;
          localStorage.setItem("nexus_session_id", sessionId);
        }
      }
    }
  } catch (err) {
    botBubble.classList.remove("typing");
    botBubble.textContent = `请求失败: ${err.message}`;
  } finally {
    sendBtn.disabled = false;
    userInput.focus();
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});
userInput.focus();
'''

# ---------------------------------------------------------------------------
# DayPlan 定义
# ---------------------------------------------------------------------------

DAYS_15_TO_24: list[DayPlan] = [
    DayPlan(
        day=15,
        title="LLM原理科普",
        phase=PHASE_2,
        epic=EPIC_E2,
        jira_stories=_jira(15, "1", "2", "3"),
        morning=[
            "站会：回顾 Day 1-14 CLI 助手，引出「为什么要懂大模型原理」",
            "理论：Transformer 直觉、预训练/微调/SFT、Token 与上下文窗口",
            "演示：GPT 类模型输入输出流程（文本 → Token → 概率 → 文本）",
        ],
        afternoon=[
            "跟敲 tiktoken_cost.py：安装 tiktoken，统计中英文混合文本 token 数",
            "对比 DeepSeek / GPT-4o-mini / Qwen 定价表，估算单次对话成本",
            "讨论：企业项目如何做 API 费用预算与限流",
        ],
        evening=[
            "阅读 OpenAI Tokenizer 文档",
            "作业：统计自己 Day 1-14 全部代码文件的 token 总量",
            "预习：Chat Completions API 请求体结构",
        ],
        code_files={"tiktoken_cost.py": TIKTOKEN_COST_PY},
        homework_desc="扩展 tiktoken_cost.py：读取指定目录下所有 .py 文件，输出总 token 数与各文件排行 Top 5，并估算调用 DeepSeek 一次全量「代码审查」的费用。",
        homework_answer_hint="使用 `Path.rglob('*.py')` 遍历；`tiktoken.get_encoding('cl100k_base')` 编码每文件内容；费用 = tokens/1e6 * 单价。注意跳过 venv 目录。",
        architecture_mermaid="""flowchart LR
    TEXT[用户文本] --> TOK[Tokenizer]
    TOK --> IDS[Token IDs]
    IDS --> LLM[大语言模型]
    LLM --> OUT[输出 Token]
    OUT --> DETOK[解码为文本]
    COST[费用估算] --> TOK""",
        narration="""林悦：「陈工，市场部要做 AI 功能，老板问一天大概花多少钱，我们答不上来。」
陈工：「先别慌。Day 15 开始，你们要学会用 token 说话——不懂 token，后面 Prompt 优化、RAG 切片、API 限流全是盲人摸象。」
你作为 Nexus 组新人，今天的任务是写出一个 **token 计数与费用估算脚本**，这是后续所有 LLM 功能的成本基线。""",
        key_concepts=["Token 与分词", "上下文窗口", "API 按量计费", "tiktoken 使用", "模型定价对比"],
        platform_touches=["为 NexusAgent v0.2 API 层建立成本意识", "后续 RAG 切片长度将直接依赖 token 统计"],
    ),
    DayPlan(
        day=16,
        title="API参数与流式输出",
        phase=PHASE_2,
        epic=EPIC_E2,
        jira_stories=_jira(16, "1", "2"),
        morning=[
            "复习 Day 15 token 概念，讲解 Chat Completions API 端点与鉴权",
            "参数详解：temperature、top_p、max_tokens、presence/frequency_penalty",
            "流式输出原理：SSE、chunk 解析、前端打字机效果",
        ],
        afternoon=[
            "跟敲 param_experiment.py：固定 prompt，对比 5 组参数输出差异",
            "跟敲 stream_output.py：实现终端流式打印",
            "配置 DEEPSEEK_API_KEY，对比 MOCK 与真实 API 行为",
        ],
        evening=[
            "阅读 DeepSeek API 文档参数说明",
            "实验：temperature=0 时多次调用是否完全一致",
            "预习：System / User / Assistant 消息角色",
        ],
        code_files={
            "param_experiment.py": PARAM_EXPERIMENT_PY,
            "stream_output.py": STREAM_OUTPUT_PY,
        },
        homework_desc="合并两个脚本为 api_playground.py：支持命令行参数 `--temp`、`--stream`，用户输入 prompt 后按配置调用 API 并输出结果与耗时。",
        homework_answer_hint="使用 `argparse`；`time.perf_counter()` 计时；流式模式逐 chunk 打印并累计 token 估算。",
        architecture_mermaid="""sequenceDiagram
    participant C as Client
    participant API as Chat API
    participant M as LLM
    C->>API: POST /v1/chat/completions
    API->>M: 推理（stream=true）
    loop SSE chunks
        M-->>API: delta content
        API-->>C: data: {...}
    end
    API-->>C: data: [DONE]""",
        narration="""陈工打开 Postman：「同一个问题，temperature 从 0 调到 1.2，答案能从『标准说明书』变成『创意文案』。API 参数就是你们调模型的旋钮。」
今天你们要亲手感受 **参数实验 + 流式输出**，这是 Day 24 Web 聊天打字机效果的底层机制。""",
        key_concepts=["Chat Completions API", "temperature/top_p", "max_tokens 截断", "SSE 流式", "urllib 调用 API"],
        platform_touches=["NexusAgent 对话服务将默认 stream=true", "参数配置将写入平台 settings.yaml"],
    ),
    DayPlan(
        day=17,
        title="Prompt基础与模板",
        phase=PHASE_2,
        epic=EPIC_E2,
        jira_stories=_jira(17, "1", "2", "3"),
        morning=[
            "Prompt 结构：System / User / Assistant 分工",
            "技巧：角色设定、任务描述、输出格式、Few-shot 示例",
            "企业场景：翻译、摘要、邮件、代码解释等 10 类高频需求",
        ],
        afternoon=[
            "跟敲 prompt_templates.py：实现 10 个可填充模板",
            "逐个场景运行 DEMO_VARIABLES 演示",
            "讨论：模板 vs 硬编码 prompt 的可维护性",
        ],
        evening=[
            "为智链科技写 3 个真实业务 Prompt 模板",
            "对比：有/无 System 提示的输出差异",
            "预习：JSON 结构化输出",
        ],
        code_files={"prompt_templates.py": PROMPT_TEMPLATES_PY},
        homework_desc="在 prompt_templates.py 基础上新增第 11 个场景「工单分类」，并支持从 YAML 文件加载模板（templates.yaml），实现热更新无需改代码。",
        homework_answer_hint="`yaml.safe_load` 读取模板；`build_messages` 优先从 YAML 查找。工单分类 system 提示需列出类别清单。",
        architecture_mermaid="""flowchart TD
    YAML[templates.yaml] --> LOAD[模板加载器]
    LOAD --> FILL[变量填充]
    VARS[业务变量] --> FILL
    FILL --> MSG[messages 数组]
    MSG --> LLM[大模型 API]
    LLM --> OUT[结构化输出]""",
        narration="""林悦发来 10 份业务需求：「客服、销售、研发各有一套话术，能不能统一成可配置模板？」
陈工：「Prompt 工程的第一课——**把魔法字符串变成可维护模板**。今天这 10 个场景，就是 NexusAgent 提示词中心的雏形。」""",
        key_concepts=["System Prompt", "模板变量填充", "Few-shot", "场景化 Prompt", "可维护性"],
        platform_touches=["platform/nexus_agent/prompts/ 将存放企业模板库", "与 Day 17 模板结构对齐"],
    ),
    DayPlan(
        day=18,
        title="Prompt进阶与JSON输出",
        phase=PHASE_2,
        epic=EPIC_E2,
        jira_stories=_jira(18, "1", "2"),
        morning=[
            "结构化输出：为什么 Agent 需要 JSON",
            "response_format / JSON mode 用法",
            "解析容错：正则提取、markdown 代码块剥离",
        ],
        afternoon=[
            "跟敲 intent_classifier.py：6 类客服意图分类",
            "测试边界 case：闲聊、多意图混合、英文输入",
            "对比 temperature=0 vs 0.7 对 JSON 稳定性的影响",
        ],
        evening=[
            "扩展：从用户消息中抽取实体（订单号、城市）",
            "阅读 JSON Schema 入门",
            "预习：Function Calling 协议",
        ],
        code_files={"intent_classifier.py": INTENT_CLASSIFIER_PY},
        homework_desc="升级意图分类器：输出增加 `sub_intent` 字段；对「查询订单 12345 并投诉物流慢」实现多意图拆分（返回 intents 数组）。",
        homework_answer_hint="修改 SYSTEM_PROMPT 要求 JSON 数组；`extract_json` 兼容 list 根节点；MOCK 模式用正则抽订单号。",
        architecture_mermaid="""flowchart LR
    USER[用户消息] --> CLS[意图分类器]
    CLS --> JSON{{JSON 输出}}
    JSON --> ROUTE[路由层]
    ROUTE --> A[订单服务]
    ROUTE --> B[FAQ服务]
    ROUTE --> C[闲聊兜底]""",
        narration="""客服主管反馈：「AI 不能只回一段话，得告诉系统该走哪个工单流程。」
今天你们要做出 **可机器解析的意图分类器**——这是 NexusAgent 路由 Agent 的第一块积木。""",
        key_concepts=["JSON 结构化输出", "意图分类", "response_format", "解析容错", "temperature=0 确定性"],
        platform_touches=["NexusAgent 消息路由将消费 intent JSON", "对接 Jira 工单类型映射"],
    ),
    DayPlan(
        day=19,
        title="Function Calling工具调用",
        phase=PHASE_2,
        epic=EPIC_E2,
        jira_stories=_jira(19, "1", "2", "3"),
        morning=[
            "Function Calling 协议：tools 定义、tool_calls、tool 角色消息",
            "手写 vs 框架：理解底层循环再学 LangChain",
            "工具设计原则：描述清晰、参数 JSON Schema、幂等性",
        ],
        afternoon=[
            "跟敲 tool_assistant.py：天气查询 + 计算器两个工具",
            "实现 dispatch_tool 与多轮 tool_calls 循环",
            "MOCK 模式验证无 API 时也能演示",
        ],
        evening=[
            "新增第三个工具：get_current_time",
            "阅读 OpenAI Function Calling 官方示例",
            "预习：Embedding 与向量检索",
        ],
        code_files={"tool_assistant.py": TOOL_ASSISTANT_PY},
        homework_desc="为 tool_assistant.py 增加 `search_faq(query)` 工具（内置 5 条 FAQ），并支持模型在一次对话中链式调用多个工具（如先查天气再计算温差）。",
        homework_answer_hint="在 TOOLS 列表追加 schema；TOOL_REGISTRY 注册实现；多轮 loop 已支持链式，重点写好工具 description。",
        architecture_mermaid="""flowchart TD
    U[用户] --> LLM[大模型]
    LLM -->|tool_calls| DISPATCH[工具分发器]
    DISPATCH --> W[get_weather]
    DISPATCH --> C[calculate]
    W --> LLM
    C --> LLM
    LLM -->|最终回复| U""",
        narration="""陈工：「模型不会查天气，但你可以教它**什么时候该调用你的函数**。Function Calling 是 Agent 的『手』。」
今天不碰任何框架，纯手写工具循环——搞懂了这个，LangChain 的 AgentExecutor 就只是语法糖。""",
        key_concepts=["Function Calling", "JSON Schema 工具定义", "tool_calls 循环", "工具注册表", "无框架实现"],
        platform_touches=["NexusAgent 工具注册中心 TOOL_REGISTRY 原型", "天气/计算器为教学用 Mock 工具"],
    ),
    DayPlan(
        day=20,
        title="Embedding与语义检索",
        phase=PHASE_2,
        epic=EPIC_E2,
        jira_stories=_jira(20, "1", "2"),
        morning=[
            "词向量直觉：从 one-hot 到稠密向量",
            "Embedding API 用法与维度",
            "余弦相似度与 Top-K 检索",
        ],
        afternoon=[
            "跟敲 similarity_matcher.py：FAQ 语义匹配",
            "对比词袋 fallback 与真实 Embedding 效果",
            "讨论：RAG 中 chunk 大小与检索质量",
        ],
        evening=[
            "尝试不同 query 表述的检索排名变化",
            "阅读 Chroma 文档简介",
            "预习：周测综合集成",
        ],
        code_files={"similarity_matcher.py": SIMILARITY_MATCHER_PY},
        homework_desc="扩展 FAQ 库至 20 条，实现混合检索：语义相似度 0.7 + 关键词匹配 0.3 加权排序，并输出可解释的匹配理由。",
        homework_answer_hint="`final_score = 0.7 * cosine + 0.3 * keyword_overlap`；理由字段说明两项得分。",
        architecture_mermaid="""flowchart LR
    Q[用户问题] --> EMB_Q[Query Embedding]
    CORPUS[FAQ 库] --> EMB_D[Doc Embeddings]
    EMB_Q --> SIM[余弦相似度]
    EMB_D --> SIM
    SIM --> TOPK[Top-K 结果]""",
        narration="""林悦：「用户不会照着 FAQ 原文提问，语义搜索得找『意思相近』的答案。」
Embedding 是 RAG 的燃料。今天先用 5 条 FAQ 跑通检索闭环，Day 25 起就上真向量库。""",
        key_concepts=["文本 Embedding", "余弦相似度", "Top-K 检索", "词袋 fallback", "FAQ 语义匹配"],
        platform_touches=["为 NexusAgent RAG 模块铺垫", "FAQ_CORPUS 将迁移至 Chroma"],
    ),
    DayPlan(
        day=21,
        title="周测综合实战",
        phase=PHASE_2,
        epic=EPIC_E2,
        jira_stories=_jira(21, "1", "2"),
        morning=[
            "周测说明：整合 Day 15-20 能力",
            "架构串讲：意图分类 → 工具/FAQ/闲聊 三分支",
            "代码 Review 规范与自测清单",
        ],
        afternoon=[
            "跟敲 integrated_chat_tools.py：REPL 综合助手",
            "自测：天气、计算、FAQ、闲聊四条路径",
            "结对 Review：互相找 bug",
        ],
        evening=[
            "周测答辩准备：3 分钟演示自己的助手",
            "整理本周笔记与踩坑清单",
            "预习：HTML/CSS/JS 基础",
        ],
        code_files={"integrated_chat_tools.py": INTEGRATED_CHAT_TOOLS_PY},
        homework_desc="在周测助手基础上增加对话历史（内存中保存最近 10 轮），闲聊分支将历史一并送入 LLM；并增加 `/help` 指令列出能力清单。",
        homework_answer_hint="维护 `history: list[dict]`；`chat_llm` 传入完整 messages；`/help` 在 REPL 入口判断。",
        architecture_mermaid="""flowchart TD
    IN[用户输入] --> INT[意图分类]
    INT -->|天气| T1[get_weather]
    INT -->|计算| T2[calculate]
    INT -->|FAQ| T3[faq_search]
    INT -->|闲聊| T4[LLM Chat]
    T1 --> OUT[统一回复]
    T2 --> OUT
    T3 --> OUT
    T4 --> OUT""",
        narration="""陈工宣布周测：「把这周学的串成一条链路。能跑、能演示、能讲清楚意图怎么走，就算过关。」
今天是 **CLI 版 Nexus 助手 MVP**，也是下周 Web 化的逻辑原型。""",
        key_concepts=["能力集成", "意图路由", "REPL 交互", "周测验收", "模块组合"],
        platform_touches=["integrated_chat_tools 逻辑将迁移至 nexus_agent/core/router.py", "v0.1 CLI → v0.2 Web 过渡节点"],
    ),
    DayPlan(
        day=22,
        title="前端速成与静态聊天",
        phase=PHASE_2,
        epic=EPIC_E2,
        jira_stories=_jira(22, "1", "2"),
        morning=[
            "HTML/CSS/JS 极速回顾：DOM、事件、fetch",
            "聊天 UI 设计：消息气泡、滚动、输入框",
            "前后端分离概念：静态页 + API",
        ],
        afternoon=[
            "搭建 frontend/index.html + style.css + chat.js",
            "实现 MOCK 模式本地聊天演示",
            "浏览器调试：Network 面板、Console 错误排查",
        ],
        evening=[
            "美化 UI：适配手机宽度",
            "预习：FastAPI 入门",
            "尝试用 Live Server 打开页面",
        ],
        code_files={
            "frontend/index.html": FRONTEND_INDEX_HTML,
            "frontend/style.css": FRONTEND_STYLE_CSS,
            "frontend/chat.js": FRONTEND_CHAT_JS,
        },
        homework_desc="为聊天界面增加 Markdown 简单渲染（粗体/代码块）和「清空对话」按钮；消息列表支持 Enter 发送、Shift+Enter 换行。",
        homework_answer_hint="`text.replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')` 简易渲染；清空即 `chatWindow.innerHTML = ''` 并恢复欢迎语。",
        architecture_mermaid="""flowchart LR
    HTML[index.html] --> JS[chat.js]
    CSS[style.css] --> HTML
    JS -->|MOCK| UI[浏览器 UI]
    JS -.->|Day23+| API[FastAPI]""",
        narration="""林悦：「老板要看『像 ChatGPT 的界面』，不要黑框框终端。」
零基础也能在一天内搭出 **能点的聊天页**。今天先 MOCK，明天接真 API。""",
        key_concepts=["HTML 结构", "CSS Flex 布局", "DOM 操作", "fetch API", "MOCK 前端"],
        platform_touches=["platform/frontend/ 目录结构预演", "NexusAgent Web 控制台 UI 雏形"],
    ),
    DayPlan(
        day=23,
        title="FastAPI后端（上）",
        phase=PHASE_2,
        epic=EPIC_E2,
        jira_stories=_jira(23, "1", "2"),
        morning=[
            "FastAPI 极速入门：路由、Pydantic、自动文档",
            "CORS 跨域配置原因与写法",
            "uvicorn 启动与热重载",
        ],
        afternoon=[
            "跟敲 api/chat_api.py：POST /api/chat",
            "对接 Day 22 前端：设置 window.NEXUS_API_BASE",
            "Swagger UI 测试接口：/docs",
        ],
        evening=[
            "增加 GET /health 监控端点",
            "阅读 FastAPI 依赖注入章节",
            "预习：SQLite 与 SSE",
        ],
        code_files={
            "api/chat_api.py": CHAT_API_PY,
            "api/__init__.py": '"""NexusAgent API 包。"""\n',
        },
        homework_desc="为 chat_api 增加请求日志中间件（打印 method/path/耗时），并新增 `/api/models` 返回当前配置的 model 名称与是否 MOCK 模式。",
        homework_answer_hint="`@app.middleware('http')` 记录 `time.perf_counter()`；`/api/models` 读取环境变量返回 JSON。",
        architecture_mermaid="""flowchart LR
    FE[Day22 前端] -->|POST /api/chat| FA[FastAPI]
    FA --> LLM[DeepSeek API]
    FA --> SW[Swagger /docs]
    FA --> HL[/health]""",
        narration="""陈工：「Python 后端首选 FastAPI——类型提示、自动文档、异步支持，企业里很常见。」
今天把 Day 21 的聊天逻辑搬上 HTTP，**前后端第一次握手**。""",
        key_concepts=["FastAPI 路由", "Pydantic 模型", "CORS", "uvicorn", "OpenAPI 文档"],
        platform_touches=["platform/nexus_agent/api/ 将基于今日结构扩展", "REST API v0.2 首个端点"],
    ),
    DayPlan(
        day=24,
        title="FastAPI后端（下）与数据库",
        phase=PHASE_2,
        epic=EPIC_E2,
        jira_stories=_jira(24, "1", "2", "3"),
        morning=[
            "SQLite 会话表设计：sessions + messages",
            "SSE 流式响应：StreamingResponse 与前端 EventSource/fetch reader",
            "静态文件托管：StaticFiles",
        ],
        afternoon=[
            "跟敲 api/database.py + api/main.py",
            "升级 frontend/chat.js 支持 SSE 流式",
            "端到端演示：多轮对话 + 刷新页面 session 保持",
        ],
        evening=[
            "第二阶段复盘：从 token 到 Web Chat 全链路",
            "整理 MR，合并 feature/day-24 分支",
            "预习 Day 25 RAG 文档上传",
        ],
        code_files={
            "api/database.py": DAY24_DATABASE_PY,
            "api/main.py": DAY24_MAIN_PY,
            "frontend/index.html": FRONTEND_INDEX_HTML,
            "frontend/style.css": FRONTEND_STYLE_CSS,
            "frontend/chat.js": DAY24_FRONTEND_CHAT_JS,
            "api/__init__.py": '"""NexusAgent API 包。"""\n',
            "requirements.txt": "fastapi>=0.110.0\nuvicorn[standard]>=0.27.0\npydantic>=2.0.0\n",
        },
        homework_desc="为 Web Chat 增加会话列表侧边栏：GET /api/sessions 展示历史会话，点击可加载 GET /api/sessions/{id}/messages 并继续对话。",
        homework_answer_hint="前端增加 sidebar DOM；`list_sessions()` 已有；加载历史后设置 `sessionId` 并渲染 messages。",
        architecture_mermaid="""flowchart TB
    FE[浏览器] -->|SSE /api/chat| API[FastAPI main.py]
    API --> DB[(SQLite)]
    API --> LLM[DeepSeek API]
    API --> STATIC[StaticFiles 前端]
    DB --> SESSIONS[sessions]
    DB --> MSGS[messages]""",
        narration="""林悦在演示会上打开浏览器：「多轮对话、流式打字、刷新不丢历史——这就是 v0.2。」
陈工补充：「SSE + SQLite，生产环境会换 Redis + PostgreSQL，但**原理今天就要搞懂**。」
第二阶段收官之日，你们交付了 **完整 Web Chat MVP**。""",
        key_concepts=["SQLite 持久化", "SSE 流式响应", "会话管理", "StaticFiles 托管", "全栈联调"],
        platform_touches=["NexusAgent v0.2 正式交付：Web Chat + SSE + SQLite", "Day 25 起在此基础上叠加 RAG"],
    ),
]
