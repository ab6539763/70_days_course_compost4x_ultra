#!/usr/bin/env python3
"""Day 30: 带引用溯源的 RAG"""
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from rag_pipeline import build_rag

def format_docs(docs) -> str:
  parts = []
  for i, d in enumerate(docs, 1):
    src = d.metadata.get("source_file", "unknown")
    parts.append(f"[{i}] ({src}) {d.page_content}")
  return "\n\n".join(parts)

if __name__ == "__main__":
  qa = build_rag()
  retriever = qa.retriever
  prompt = ChatPromptTemplate.from_template(
    "上下文：\n{context}\n\n问题：{question}\n请回答并标注引用编号。"
  )
  chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt | qa.chain.llm | StrOutputParser()
  )
  print(chain.invoke("报销流程是什么？"))
