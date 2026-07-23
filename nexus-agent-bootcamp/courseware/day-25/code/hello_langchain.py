#!/usr/bin/env python3
"""Day 25: LangChain 入门 — ChatOpenAI 最小调用"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def build_llm() -> ChatOpenAI:
    # OpenAI 兼容协议连接 DeepSeek
    return ChatOpenAI(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        temperature=0.3,
    )

def main() -> None:
    llm = build_llm()
    messages = [
        SystemMessage(content="你是智链科技 Nexus 项目 AI 助教，回答简洁专业。"),
        HumanMessage(content="用三句话介绍 LangChain 的核心价值。"),
    ]
    if os.getenv("DEEPSEEK_API_KEY"):
        print(llm.invoke(messages).content)
    else:
        print("[MOCK] LangChain 统一 Model/Prompt/Chain 抽象，降低 LLM 应用开发成本。")

if __name__ == "__main__":
    main()
