#!/usr/bin/env python3
"""Day 28: RecursiveCharacterTextSplitter 文档切分"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

SAMPLE = """
# Nexus 员工手册
## 考勤制度
员工应按时打卡。迟到三次记警告。
## 年假
工作满一年享 5 天年假。
## 报销
差旅费需附发票，30 日内提交。
""" * 3

def split_document(text: str, chunk_size: int = 200, overlap: int = 50) -> list[str]:
  splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=overlap,
    separators=["\n## ", "\n", "。", " "],
  )
  return splitter.split_text(text)

if __name__ == "__main__":
  chunks = split_document(SAMPLE)
  for i, ch in enumerate(chunks):
    print(f"--- chunk {i} ({len(ch)} chars) ---")
    print(ch[:120])
