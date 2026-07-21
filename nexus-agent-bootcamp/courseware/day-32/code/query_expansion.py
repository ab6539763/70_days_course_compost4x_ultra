#!/usr/bin/env python3
"""Day 32: 多查询扩展检索"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
  "将用户问题改写成 3 个不同表述的检索查询，每行一个：\n{question}"
)
llm = ChatOpenAI(
  model="deepseek-chat",
  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
expand_chain = prompt | llm | StrOutputParser()

def multi_query(question: str) -> list[str]:
  text = expand_chain.invoke({"question": question})
  return [line.strip() for line in text.splitlines() if line.strip()][:3]

if __name__ == "__main__":
  print(multi_query("员工年假怎么算？"))
