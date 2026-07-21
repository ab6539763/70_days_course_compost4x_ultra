"""Day 60 — 混合检索器"""
from dataclasses import dataclass


@dataclass
class RetrievalResult:
    content: str
    score: float
    source: str


class HybridRetriever:
    """向量检索 + 关键词检索融合（教学简化版）"""

    def __init__(self, top_k: int = 5) -> None:
        self.top_k = top_k
        self._docs = [
            RetrievalResult("重置密码请进入管理后台系统设置", 0.92, "faq.md"),
            RetrievalResult("RAG 检索需确保 Chroma 在线", 0.85, "ops.md"),
        ]

    def search(self, query: str) -> list[RetrievalResult]:
        """按关键词匹配模拟混合检索"""
        results = [d for d in self._docs if any(k in d.content for k in query.split())]
        return sorted(results, key=lambda r: r.score, reverse=True)[: self.top_k]
