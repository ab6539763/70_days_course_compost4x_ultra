#!/usr/bin/env python3
"""企业知识库项目 — 配置模块"""
import os
from pathlib import Path

# 数据与向量库路径
DATA_DIR = Path(os.getenv("NEXUS_DATA_DIR", "data"))
CHROMA_DIR = DATA_DIR / "chroma_enterprise"
UPLOAD_DIR = DATA_DIR / "uploads"

# 模型配置
LLM_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
API_BASE = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# RAG 超参数
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
TOP_K = 4
