"""Day 62 — 集成所有模块的完整入口"""
from app.main import app
from app.auth.router import router as auth_router
from app.rag.router import router as rag_router
from app.agent.router import router as agent_router
from app.api.router import api_router
from app.api.middleware import RequestLogMiddleware

app.include_router(auth_router)
app.include_router(rag_router)
app.include_router(agent_router)
app.include_router(api_router)
app.add_middleware(RequestLogMiddleware)
