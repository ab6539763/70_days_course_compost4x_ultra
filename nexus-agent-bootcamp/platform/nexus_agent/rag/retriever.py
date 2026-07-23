"""向量检索器接口"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Document:
    id: str
    content: str
    metadata: dict


class VectorRetriever:
    """向量检索 — 生产环境对接 Chroma/Milvus"""

    def __init__(self) -> None:
        self._store: List[Tuple[List[float], Document]] = []

    def add(self, embedding: List[float], doc: Document) -> None:
        self._store.append((embedding, doc))

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Document]:
        def cosine(a: List[float], b: List[float]) -> float:
            dot = sum(x * y for x, y in zip(a, b))
            na = sum(x * x for x in a) ** 0.5
            nb = sum(x * x for x in b) ** 0.5
            return dot / (na * nb + 1e-9)

        scored = [(cosine(query_embedding, emb), doc) for emb, doc in self._store]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]
