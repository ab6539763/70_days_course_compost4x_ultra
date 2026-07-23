"""Day 64 — RAG 模块测试"""
from app.rag.ingest import chunk_text
from app.rag.retriever import HybridRetriever


def test_chunk_text():
    text = "a" * 1000
    chunks = chunk_text(text, chunk_size=200, overlap=20)
    assert len(chunks) >= 5


def test_retriever():
    results = HybridRetriever().search("重置密码")
    assert len(results) > 0
