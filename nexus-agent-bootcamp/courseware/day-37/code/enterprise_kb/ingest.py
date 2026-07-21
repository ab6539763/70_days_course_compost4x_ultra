#!/usr/bin/env python3
"""企业知识库 — 文档入库管道"""
from pathlib import Path
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import UPLOAD_DIR, CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, API_KEY, API_BASE, EMBED_MODEL

def load_documents(src: Path) -> list:
  if src.is_file():
    return TextLoader(str(src), encoding="utf-8").load()
  loader = DirectoryLoader(str(src), glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
  return loader.load()

def ingest(src: Path) -> int:
  docs = load_documents(src)
  splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
  chunks = splitter.split_documents(docs)
  emb = OpenAIEmbeddings(model=EMBED_MODEL, api_key=API_KEY or "mock", base_url=API_BASE)
  Chroma.from_documents(chunks, embedding=emb, persist_directory=str(CHROMA_DIR))
  return len(chunks)

if __name__ == "__main__":
  UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
  sample = UPLOAD_DIR / "policy.txt"
  if not sample.exists():
    sample.write_text("智链科技员工手册：年假5天，报销需发票。", encoding="utf-8")
  print("入库 chunks:", ingest(UPLOAD_DIR))
