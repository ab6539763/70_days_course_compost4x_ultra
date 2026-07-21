#!/usr/bin/env python3
"""Day 30: 完整 RAG 管道"""
import os
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

PROMPT = PromptTemplate(
  template="""根据以下上下文回答问题，不知道就说不知道。
上下文：
{context}
问题：{question}
回答（中文，简洁）：""",
  input_variables=["context", "question"],
)

def build_rag(persist_dir: str = "./data/chroma_handbook") -> RetrievalQA:
  emb = OpenAIEmbeddings(
    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
  )
  vs = Chroma(persist_directory=persist_dir, embedding_function=emb)
  retriever = vs.as_retriever(search_kwargs={"k": 3})
  llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
  )
  return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

if __name__ == "__main__":
  qa = build_rag()
  print(qa.invoke({"query": "年假有几天？"}))
