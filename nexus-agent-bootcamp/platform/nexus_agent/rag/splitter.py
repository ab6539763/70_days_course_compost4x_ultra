"""文档分割 — RecursiveCharacterTextSplitter 教学实现"""
from __future__ import annotations
from typing import List


def recursive_split(text: str, chunk_size: int = 500, chunk_overlap: int = 50, separators: List[str] | None = None) -> List[str]:
    """按分隔符递归切分，保证 chunk 不超过 chunk_size"""
    if separators is None:
        separators = ["\n\n", "\n", "。", " ", ""]
    if len(text) <= chunk_size:
        return [text] if text.strip() else []
    for sep in separators:
        if sep in text:
            parts = text.split(sep)
            chunks: List[str] = []
            current = ""
            for p in parts:
                candidate = current + sep + p if current else p
                if len(candidate) <= chunk_size:
                    current = candidate
                else:
                    if current:
                        chunks.extend(recursive_split(current, chunk_size, chunk_overlap, separators[1:]))
                    current = p
            if current:
                chunks.extend(recursive_split(current, chunk_size, chunk_overlap, separators[1:]))
            return chunks
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size - chunk_overlap)]
