#!/usr/bin/env python3
"""Day 27: ConversationBufferMemory 多轮对话"""
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

def build_chain() -> ConversationChain:
  # 缓冲全部历史消息
  memory = ConversationBufferMemory()
  llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
  )
  return ConversationChain(llm=llm, memory=memory, verbose=True)

if __name__ == "__main__":
  chain = build_chain()
  print(chain.predict(input="我叫小明，在智链科技实习。"))
  print(chain.predict(input="我叫什么？在哪实习？"))
