#!/usr/bin/env python3
"""Day 29: 切分文档并写入 Chroma"""
from pathlib import Path
from doc_loader import load_and_split
from chroma_basics import build_vectorstore

if __name__ == "__main__":
  p = Path("data/handbook.txt")
  chunks = load_and_split(p)
  texts = [c.page_content for c in chunks]
  vs = build_vectorstore(texts, persist_dir="./data/chroma_handbook")
  print("入库完成，共", len(texts), "条")
