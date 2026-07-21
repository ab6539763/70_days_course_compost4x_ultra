#!/usr/bin/env python3
"""企业知识库 — 检索与问答"""
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from config import CHROMA_DIR, API_KEY, API_BASE, EMBED_MODEL, LLM_MODEL, TOP_K

def build_qa() -> RetrievalQA:
  emb = OpenAIEmbeddings(model=EMBED_MODEL, api_key=API_KEY or "mock", base_url=API_BASE)
  vs = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=emb)
  retriever = vs.as_retriever(search_kwargs={"k": TOP_K})
  llm = ChatOpenAI(model=LLM_MODEL, api_key=API_KEY or "mock", base_url=API_BASE, temperature=0.1)
  return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

if __name__ == "__main__":
  qa = build_qa()
  r = qa({"query": "年假有几天？"})
  print(r["result"])
