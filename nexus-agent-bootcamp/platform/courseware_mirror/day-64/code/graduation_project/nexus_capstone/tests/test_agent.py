"""Day 64 — Agent 模块测试"""
from app.agent.graph import run_agent


def test_agent_with_retrieval():
    answer = run_agent("如何重置密码？")
    assert "知识库" in answer or "密码" in answer


def test_agent_fallback():
    answer = run_agent("今天天气怎么样")
    assert len(answer) > 0
