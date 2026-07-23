#!/usr/bin/env python3
"""Day 28: chunk_size / overlap 对比实验"""
from text_splitter import split_document, SAMPLE

if __name__ == "__main__":
  for size, ov in [(100, 20), (300, 50), (500, 100)]:
    chunks = split_document(SAMPLE, size, ov)
    print(f"size={size} overlap={ov} -> {len(chunks)} chunks")
