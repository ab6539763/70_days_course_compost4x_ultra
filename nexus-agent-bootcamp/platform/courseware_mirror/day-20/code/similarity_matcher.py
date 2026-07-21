#!/usr/bin/env python3
"""
Day 20 实操：文本 Embedding 与语义相似度匹配
演示向量表示、余弦相似度，以及简单 FAQ 检索。
无 API 时使用 TF-IDF 风格词袋向量作为 fallback。
"""
from __future__ import annotations

import json
import math
import os
import re
import urllib.error
import urllib.request
from collections import Counter
from typing import Any

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

FAQ_CORPUS = [
    {"id": "faq-01", "question": "NexusAgent 支持哪些大模型？", "answer": "支持 DeepSeek、Qwen、OpenAI 兼容 API。"},
    {"id": "faq-02", "question": "如何上传企业知识库文档？", "answer": "Day 25 起支持 PDF/Word 上传并向量化。"},
    {"id": "faq-03", "question": "是否支持私有化部署？", "answer": "支持 Docker 私有化，Day 56 详解。"},
    {"id": "faq-04", "question": "API 调用如何计费？", "answer": "按 token 计费，可在控制台查看用量。"},
    {"id": "faq-05", "question": "能否对接飞书机器人？", "answer": "Day 45 将讲解 Webhook 与飞书集成。"},
]


def tokenize(text: str) -> list[str]:
    """简单分词：中文按字、英文按单词。"""
    chars = re.findall(r"[\u4e00-\u9fff]", text)
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return chars + words


def bag_of_words_vector(text: str, vocab: dict[str, int]) -> list[float]:
    """词袋向量（教学 fallback）。"""
    counts = Counter(tokenize(text))
    return [float(counts.get(w, 0)) for w in vocab]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算余弦相似度。"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def build_vocab(texts: list[str]) -> dict[str, int]:
    """构建词表。"""
    vocab: dict[str, int] = {}
    for t in texts:
        for tok in set(tokenize(t)):
            if tok not in vocab:
                vocab[tok] = len(vocab)
    return vocab


def get_embedding_api(text: str) -> list[float] | None:
    """调用 Embedding API；失败返回 None。"""
    if not API_KEY:
        return None
    payload = {"model": EMBED_MODEL, "input": text}
    req = urllib.request.Request(
        f"{API_BASE}/v1/embeddings",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["data"][0]["embedding"]
    except (urllib.error.URLError, KeyError, json.JSONDecodeError):
        return None


def embed_texts(texts: list[str]) -> list[list[float]]:
    """批量向量化；优先 API，否则词袋。"""
    api_vecs = [get_embedding_api(t) for t in texts]
    if all(v is not None for v in api_vecs):
        return api_vecs  # type: ignore[list-item]

    print("  [INFO] 使用本地词袋向量（未配置 API 或 Embedding 不可用）")
    vocab = build_vocab(texts)
    return [bag_of_words_vector(t, vocab) for t in texts]


def search_faq(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """语义检索 FAQ，返回 top_k 条。"""
    questions = [item["question"] for item in FAQ_CORPUS]
    all_texts = questions + [query]
    vectors = embed_texts(all_texts)
    query_vec = vectors[-1]
    doc_vecs = vectors[:-1]

    scored = []
    for item, vec in zip(FAQ_CORPUS, doc_vecs):
        score = cosine_similarity(query_vec, vec)
        scored.append({**item, "score": round(score, 4)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def main() -> None:
    queries = [
        "你们平台能接什么模型？",
        "怎么把公司文档放进去？",
        "本地服务器能装吗？",
    ]
    print("=" * 60)
    print("Day 20 — Embedding 语义相似度匹配")
    print("=" * 60)
    for q in queries:
        print(f"\n查询: {q}")
        results = search_faq(q)
        for r in results:
            print(f"  [{r['score']:.4f}] {r['question']}")
            print(f"         → {r['answer']}")


if __name__ == "__main__":
    main()
