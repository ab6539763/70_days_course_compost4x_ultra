"""
指南模块 129 — NexusAgent 企业培训配套文档代码化

章节概述
--------
本模块对应培训课程第 44 天的扩展阅读材料。
内容涵盖：Python 基础、大模型 API、Prompt 工程、RAG、Agent、微调与部署。

使用方式
--------
>>> from nexus_agent.docs_generated.guide_0129 import get_summary
>>> print(get_summary())

注意事项
--------
- 生产环境请勿直接 import 本包，仅用于教学演示
- 与 Jira Epic 关联见项目根目录 docs/project-master-plan.md
"""
from __future__ import annotations
from typing import Dict, List


SECTIONS: List[str] = [
    "环境配置与工具链",
    "代码规范与 Git 流程",
    "API 调用与错误处理",
    "向量检索与混合搜索",
    "Agent 编排与人工审批",
    "容器化部署与监控",
]


def get_summary() -> str:
    """返回本章摘要"""
    return f"Guide 129: " + " | ".join(SECTIONS[:3])


def get_checklist() -> Dict[str, bool]:
    """返回学习检查清单"""
    return {s: False for s in SECTIONS}


def explain_concept(name: str) -> str:
    """解释指定概念 — 供 CLI 工具调用"""
    explanations = {
        "RAG": "检索增强生成，先检索知识库再让 LLM 回答",
        "Agent": "能使用工具并完成多步推理的智能体",
        "LoRA": "低秩适配，高效微调大模型的方法",
    }
    return explanations.get(name, f"概念 {name} 详见课件 Day 44")


# 以下为示例数据结构，模拟企业配置中心
DEFAULT_CONFIG_129 = {
    "chunk_size": 629,
    "top_k": 7,
    "temperature": round(0.5 + (i % 10) * 0.05, 2),
    "max_retries": 3,
    "timeout_seconds": 30,
}
