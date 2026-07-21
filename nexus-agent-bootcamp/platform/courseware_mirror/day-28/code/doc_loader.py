#!/usr/bin/env python3
"""Day 28: 文档加载与元数据"""
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split(path: Path) -> list:
  loader = TextLoader(str(path), encoding="utf-8")
  docs = loader.load()
  splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=60)
  chunks = splitter.split_documents(docs)
  for c in chunks:
    c.metadata["source_file"] = path.name
  return chunks

if __name__ == "__main__":
  p = Path("data/handbook.txt")
  p.parent.mkdir(exist_ok=True)
  if not p.exists():
    p.write_text("Nexus 平台支持 RAG 知识库问答。", encoding="utf-8")
  for doc in load_and_split(p):
    print(doc.metadata, doc.page_content[:60])
