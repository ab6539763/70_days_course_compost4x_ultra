"""Day 63 — 挂载静态前端到 FastAPI"""
from fastapi.staticfiles import StaticFiles
from pathlib import Path

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


def mount_frontend(app) -> None:
    """将 frontend/ 目录挂载到根路径"""
    if FRONTEND_DIR.exists():
        app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
