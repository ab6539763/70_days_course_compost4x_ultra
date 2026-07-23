#!/usr/bin/env python3
"""Day 32: HyDE — 先生成假设文档再检索（占位）"""
import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
  model="deepseek-chat",
  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)

def hyde_query(question: str) -> str:
  # 生成一段「假设性答案」作为检索 query
  return f"假设文档：关于「{question}」的标准解答段落..."

if __name__ == "__main__":
  print(hyde_query("远程办公政策"))
