#!/usr/bin/env python3
"""Day 46: Agent FastAPI 服务"""
from fastapi import FastAPI
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nexus.agent")

app = FastAPI(title="Nexus Agent Service")

class ChatRequest(BaseModel):
  message: str
  session_id: str = "default"

@app.get("/health")
def health():
  return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
  logger.info("chat session=%s msg=%s", req.session_id, req.message[:80])
  # 接入 LangGraph app
  answer = f"Agent 回复: {req.message}"
  return {"answer": answer, "session_id": req.session_id}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8001)
