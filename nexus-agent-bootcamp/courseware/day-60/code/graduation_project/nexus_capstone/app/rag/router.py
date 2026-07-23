"""Day 60 — 知识库 API"""
from fastapi import APIRouter, UploadFile
from app.rag.retriever import HybridRetriever

router = APIRouter(prefix="/api/v1/knowledge", tags=["知识库"])
retriever = HybridRetriever()


@router.post("/upload")
async def upload_document(file: UploadFile) -> dict:
    content = (await file.read()).decode("utf-8")
    from app.rag.ingest import chunk_text
    chunks = chunk_text(content)
    return {"filename": file.filename, "chunks": len(chunks)}


@router.get("/search")
def search_knowledge(q: str) -> dict:
    results = retriever.search(q)
    return {"query": q, "results": [{"content": r.content, "score": r.score, "source": r.source} for r in results]}
