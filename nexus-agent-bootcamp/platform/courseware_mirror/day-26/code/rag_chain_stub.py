#!/usr/bin/env python3
"""Day 26: RAG 链骨架（检索占位）"""
import os
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

def fake_retrieve(query: str) -> str:
    return f"[占位上下文] 关于「{query}」的企业文档摘要。"

prompt = ChatPromptTemplate.from_template(
    "根据上下文回答。\n上下文：{context}\n问题：{question}"
)
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
rag_chain = (
    {"context": RunnableLambda(fake_retrieve), "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)
if __name__ == "__main__":
    print(rag_chain.invoke("年假政策是什么？"))
