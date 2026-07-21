#!/usr/bin/env python3
"""
Day 23 实操：FastAPI 聊天 API（上半）
提供 REST 端点 /api/chat，支持 CORS，可对接 Day 22 前端。
运行: uvicorn api.chat_api:app --reload --port 8000
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

app = FastAPI(title="NexusAgent Chat API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str | None = None
    model: str = MODEL


def call_llm(prompt: str) -> str:
    if not API_KEY:
        return f"【MOCK FastAPI】已收到: {prompt[:100]}"
    payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    req = urllib.request.Request(
        f"{API_BASE}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
        return f"LLM 调用失败: {exc}"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "nexus-chat-api"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    reply = call_llm(req.message)
    return ChatResponse(reply=reply, session_id=req.session_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.chat_api:app", host="0.0.0.0", port=8000, reload=True)
