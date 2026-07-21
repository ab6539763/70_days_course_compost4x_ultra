#!/usr/bin/env python3
"""Day 26: LCEL 基础链与流式输出"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("用一句话解释：{concept}")
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
chain = prompt | llm | StrOutputParser()

if __name__ == "__main__":
    print(chain.invoke({"concept": "LCEL"}))
    for chunk in chain.stream({"concept": "Runnable"}):
        print(chunk, end="", flush=True)
    print()
