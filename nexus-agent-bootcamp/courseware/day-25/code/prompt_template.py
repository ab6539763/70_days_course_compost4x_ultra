#!/usr/bin/env python3
"""Day 25: PromptTemplate 与变量注入"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，负责解答{domain}相关问题。"),
    ("human", "{question}"),
])
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
chain = prompt.partial(role="Nexus 知识库助手", domain="RAG") | llm

if __name__ == "__main__":
    result = chain.invoke({"question": "什么是向量检索？"})
    print(getattr(result, "content", result))
