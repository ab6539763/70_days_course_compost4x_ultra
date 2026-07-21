#!/usr/bin/env python3
"""Day 27: ConversationBufferWindowMemory 滑动窗口"""
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

memory = ConversationBufferWindowMemory(k=2)  # 仅保留最近 2 轮
llm = ChatOpenAI(
  model="deepseek-chat",
  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
chain = ConversationChain(llm=llm, memory=memory)

if __name__ == "__main__":
  for q in ["A", "B", "C", "你还记得 A 吗？"]:
    print("Q:", q)
    print("A:", chain.predict(input=q)[:80])
