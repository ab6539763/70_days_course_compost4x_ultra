#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt 模板 f-string 演示 prompt_fstring.py — Day 2 核心技能
f-string 是后续 Prompt 工程、API messages 组装的基石
企业场景：客服意图分类、RAG 问答模板、Agent 系统提示词
"""

from __future__ import annotations

from typing import Any

# 系统角色设定 — 后续会作为 API messages[0] 的 content
SYSTEM_ROLE = "你是智链科技 NexusAgent 知识库助手，回答需简洁、准确、可溯源。"

# 用户问题占位
user_question = "RAG 检索的 chunk_size 一般设多少？"

# 检索到的上下文片段（Day 30 会从向量库真实获取）
context_snippets = [
    "推荐 chunk_size 在 300-800 字符之间，需结合文档类型调优。",
    "技术文档可适当增大，对话记录宜减小。",
]

# 将列表用换行拼接为单个上下文字符串
context_block = "\n".join(f"- {s}" for s in context_snippets)

# 基础 f-string：嵌入变量
simple_prompt = f"用户问题：{user_question}"

# 多行 f-string：三引号保留换行（企业 Prompt 标准写法）
rag_prompt = f"""{SYSTEM_ROLE}

## 检索上下文
{context_block}

## 用户问题
{user_question}

## 回答要求
1. 仅基于上述上下文回答，不知道则说明
2. 在末尾标注引用编号
"""

# 表达式在 {} 内：可直接调用方法、运算
summary_line = f"共注入 {len(context_snippets)} 条上下文，合计约 {len(context_block)} 字符"

# 格式化数字：:.2f 保留两位小数（成本估算常用）
token_estimate = len(rag_prompt) / 4  # 粗估 1 token ≈ 4 字符（中文偏少）
cost_line = f"预估 token ≈ {token_estimate:.0f}，费用约 ¥{token_estimate / 1000 * 0.002:.6f}"

# f-string 对齐与填充（生成表格化日志）
def build_message_row(role: str, content_preview: str, width: int = 40) -> str:
    """生成固定宽度的消息预览行，用于调试日志"""
    preview = content_preview.replace("\n", " ")[:width]
    return f"| {role:<10} | {preview:<{width}} |"


# 字典解包：**dict 在 f-string 中展开键值（Python 3.11+ 简写需注意版本）
model_params: dict[str, Any] = {
    "temperature": 0.3,
    "max_tokens": 1024,
    "top_p": 0.9,
}
params_line = f"模型参数: temp={model_params['temperature']}, max_tokens={model_params['max_tokens']}"

# 转义花括号：字面量 { } 需双写 {{ }}
literal_brace_demo = f"JSON 示例: {{\"role\": \"user\", \"content\": \"...\"}}"


def build_chat_messages(user_msg: str, context: str) -> list[dict[str, str]]:
    """
    组装 OpenAI/DeepSeek 兼容的 messages 列表
    Day 12 将直接用于 API 请求体
    """
    system_content = f"""{SYSTEM_ROLE}

参考上下文：
{context}
"""
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_msg},
    ]


def main() -> None:
    print("=" * 60)
    print("  Prompt f-string 模板演示 — Day 2")
    print("=" * 60)
    print("\n【简单 Prompt】")
    print(simple_prompt)
    print("\n【完整 RAG Prompt 模板】")
    print(rag_prompt)
    print("-" * 60)
    print(summary_line)
    print(cost_line)
    print(params_line)
    print(literal_brace_demo)
    print("-" * 60)
    print("【消息表格预览】")
    print(build_message_row("system", SYSTEM_ROLE))
    print(build_message_row("user", user_question))
    print("-" * 60)
    messages = build_chat_messages(user_question, context_block)
    print(f"【API messages 结构】共 {len(messages)} 条")
    for i, m in enumerate(messages):
        preview = m["content"][:80].replace("\n", " ")
        print(f"  [{i}] role={m['role']!r} content={preview}...")
    print("=" * 60)
    print("✅ prompt_fstring 运行成功 — 此技能将贯穿 70 天课程")


if __name__ == "__main__":
    main()
