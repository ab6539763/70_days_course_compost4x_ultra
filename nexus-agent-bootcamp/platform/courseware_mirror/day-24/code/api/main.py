#!/usr/bin/env python3
"""
Day 24 实操：FastAPI 完整 Web Chat（下半）
特性：SSE 流式输出、SQLite 会话持久化、静态前端托管。
运行: python -m api.main  或  python api/main.py
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from api.database import add_message, create_session, get_messages, init_db, list_sessions

API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend"

app = FastAPI(title="NexusAgent Web Chat", version="0.2.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str | None = None
    stream: bool = False


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.2.1"}


@app.get("/api/sessions")
def api_list_sessions() -> list[dict]:
    return list_sessions()


@app.get("/api/sessions/{session_id}/messages")
def api_get_messages(session_id: str) -> list[dict]:
    return get_messages(session_id)


def _build_llm_messages(session_id: str, user_msg: str) -> list[dict[str, str]]:
    history = get_messages(session_id, limit=20)
    messages = [{"role": "system", "content": "你是智链科技 NexusAgent 助手，回答简洁专业。"}]
    for m in history:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": user_msg})
    return messages


def _stream_llm(messages: list[dict[str, str]]) -> list[str]:
    if not API_KEY:
        return list(f"【MOCK SSE】{messages[-1]['content'][:80]} 的回复已写入数据库。")
    payload = {"model": MODEL, "messages": messages, "stream": True, "temperature": 0.7}
    req = urllib.request.Request(
        f"{API_BASE}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method="POST",
    )
    tokens: list[str] = []
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8").strip()
                if not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str == "[DONE]":
                    break
                chunk = json.loads(data_str)
                content = chunk["choices"][0].get("delta", {}).get("content", "")
                if content:
                    tokens.append(content)
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as exc:
        tokens = [f"流式调用失败: {exc}"]
    return tokens


async def sse_generator(session_id: str, user_msg: str) -> AsyncGenerator[str, None]:
    add_message(session_id, "user", user_msg)
    messages = _build_llm_messages(session_id, user_msg)
    messages = messages[:-1]
    messages.append({"role": "user", "content": user_msg})

    full_reply: list[str] = []
    for token in _stream_llm(messages):
        full_reply.append(token)
        payload = json.dumps({"token": token, "session_id": session_id}, ensure_ascii=False)
        yield f"data: {payload}\n\n"
        time.sleep(0.01)

    reply_text = "".join(full_reply)
    add_message(session_id, "assistant", reply_text)
    yield f"data: {json.dumps({'done': True, 'reply': reply_text}, ensure_ascii=False)}\n\n"


@app.post("/api/chat")
async def api_chat(req: ChatRequest) -> StreamingResponse | dict:
    session_id = req.session_id or create_session(title=req.message[:20])
    if req.stream:
        return StreamingResponse(
            sse_generator(session_id, req.message),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
    add_message(session_id, "user", req.message)
    tokens = _stream_llm(_build_llm_messages(session_id, req.message))
    reply = "".join(tokens)
    add_message(session_id, "assistant", reply)
    return {"reply": reply, "session_id": session_id}


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    print("启动 NexusAgent Web Chat → http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
