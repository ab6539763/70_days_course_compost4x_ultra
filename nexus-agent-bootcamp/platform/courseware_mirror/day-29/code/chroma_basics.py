#!/usr/bin/env python3
"""Day 29: Chroma 向量库基础"""
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def build_vectorstore(texts: list[str], persist_dir: str = "./chroma_db") -> Chroma:
  embeddings = OpenAIEmbeddings(
    model=os.getenv("EMBED_MODEL", "text-embedding-3-small"),
    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
  )
  return Chroma.from_texts(texts, embedding=embeddings, persist_directory=persist_dir)

if __name__ == "__main__":
  faq = ["Nexus 支持 DeepSeek", "年假 5 天起", "报销需发票"]
  vs = build_vectorstore(faq)
  results = vs.similarity_search("用什么模型？", k=2)
  for r in results:
    print(r.page_content)
