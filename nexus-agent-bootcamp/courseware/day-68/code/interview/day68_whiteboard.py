#!/usr/bin/env python3
"""Day 68 — 白板编程：简化版 RAG Pipeline（面试手写）"""

def rag_pipeline(query: str, documents: list[str], top_k: int = 3) -> str:
    """面试白板版 RAG：关键词匹配 + 模板回答"""
    # Step 1: 检索（简化为关键词匹配）
    scored = []
    for doc in documents:
        score = sum(1 for word in query.split() if word in doc)
        scored.append((score, doc))
    scored.sort(reverse=True)
    top_docs = [doc for _, doc in scored[:top_k]]

    # Step 2: 组装上下文
    context = "\n".join(top_docs) if top_docs else "无相关文档"

    # Step 3: 生成回答（生产环境调用 LLM）
    return f"根据知识库资料：\n{context}\n\n以上信息供参考。"


if __name__ == "__main__":
    docs = ["重置密码请进入管理后台", "RAG 需要 Chroma 在线", "API 限流默认 100/min"]
    print(rag_pipeline("如何重置密码", docs))
