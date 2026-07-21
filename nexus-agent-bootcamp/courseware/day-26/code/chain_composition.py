#!/usr/bin/env python3
"""Day 26: RunnableLambda 链组合"""
import os
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def uppercase(text: str) -> str:
    return text.upper()

prompt = ChatPromptTemplate.from_template("总结工单：{ticket}")
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
chain = (
    {"ticket": RunnablePassthrough()} | prompt | llm
    | RunnableLambda(lambda m: m.content) | RunnableLambda(uppercase)
)
if __name__ == "__main__":
    print(chain.invoke("客户反馈登录慢，已复现。"))
