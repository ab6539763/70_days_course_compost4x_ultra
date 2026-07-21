#!/usr/bin/env python3
"""Day 35: LlamaIndex QueryEngine 概念"""
try:
  from llama_index.core import VectorStoreIndex, Document
  HAS_LLAMA = True
except ImportError:
  HAS_LLAMA = False

def build_engine(texts: list[str]):
  if not HAS_LLAMA:
    from llamaindex_basics import mock_index, query
    idx = mock_index(texts)
    return lambda q: query(idx, q)
  docs = [Document(text=t) for t in texts]
  index = VectorStoreIndex.from_documents(docs)
  return index.as_query_engine()

if __name__ == "__main__":
  engine = build_engine(["Nexus 支持 RAG", "Agent 编排用 LangGraph"])
  print(engine("RAG 用什么？"))
