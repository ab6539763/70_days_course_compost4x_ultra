"""Day 61 — LangGraph Agent 编排"""
from typing import TypedDict


class AgentState(TypedDict):
    """Agent 状态机：记录对话与工具调用上下文"""
    messages: list[dict]
    tool_results: list[str]
    final_answer: str


def search_tool(query: str) -> str:
    """模拟知识库检索工具"""
    from app.rag.retriever import HybridRetriever
    results = HybridRetriever().search(query)
    return "\n".join(r.content for r in results) or "未找到相关内容"


def run_agent(user_query: str) -> str:
    """
    简化版 ReAct Agent 流程：
    1. 判断是否需要检索
    2. 调用工具
    3. 生成最终回答
    """
    state: AgentState = {"messages": [{"role": "user", "content": user_query}], "tool_results": [], "final_answer": ""}

    # 步骤 1: 检索增强
    if any(kw in user_query for kw in ("如何", "怎么", "什么是")):
        tool_output = search_tool(user_query)
        state["tool_results"].append(tool_output)

    # 步骤 2: 合成回答（生产环境调用 LLM）
    context = state["tool_results"][0] if state["tool_results"] else ""
    state["final_answer"] = f"根据知识库：{context}" if context else f"关于「{user_query}」，建议联系人工支持。"
    return state["final_answer"]
