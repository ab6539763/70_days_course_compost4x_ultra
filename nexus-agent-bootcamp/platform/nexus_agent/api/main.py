"""NexusAgent FastAPI 入口 — Day24+ 企业版"""
from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="NexusAgent API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "nexus-agent"}


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    from nexus_agent.llm.deepseek import DeepSeekLLM
    llm = DeepSeekLLM()
    reply = llm.chat([{"role": "user", "content": req.message}])
    return ChatResponse(reply=reply, session_id=req.session_id or "default")
