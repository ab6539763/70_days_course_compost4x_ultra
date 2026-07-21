"""Day 62 — 聚合路由注册"""
from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/status")
def api_status() -> dict:
    return {
        "version": "1.0.0",
        "modules": {
            "auth": "ready",
            "rag": "ready",
            "agent": "ready",
        },
    }
