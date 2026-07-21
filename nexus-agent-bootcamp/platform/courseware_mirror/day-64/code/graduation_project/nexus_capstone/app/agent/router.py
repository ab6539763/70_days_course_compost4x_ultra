"""Day 61 — Agent 对话 API"""
from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.graph import run_agent

router = APIRouter(prefix="/api/v1/agent", tags=["Agent"])


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def agent_chat(req: ChatRequest) -> dict:
    answer = run_agent(req.message)
    return {"answer": answer, "agent": "nexus-capstone-v1"}
