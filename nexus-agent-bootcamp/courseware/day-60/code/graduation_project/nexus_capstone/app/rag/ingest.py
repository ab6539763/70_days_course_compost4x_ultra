"""Day 60 — 文档入库与向量化"""
from pathlib import Path


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """滑动窗口分块，保留上下文重叠"""
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size - overlap
    return chunks


def ingest_document(path: Path, collection_name: str = "capstone_kb") -> int:
    """读取文档并写入 Chroma（Mock 模式返回块数）"""
    text = path.read_text(encoding="utf-8")
    chunks = chunk_text(text)
  # 生产: chroma_client.get_or_create_collection(collection_name).add(...)
    print(f"[ingest] {path.name}: {len(chunks)} 块 -> {collection_name}")
    return len(chunks)
