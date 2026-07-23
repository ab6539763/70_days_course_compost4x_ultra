#!/usr/bin/env python3
"""企业知识库 — FastAPI 接口"""
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
from ingest import ingest
from retriever import build_qa
from config import UPLOAD_DIR

app = FastAPI(title="Nexus Enterprise KB")
qa_chain = None

class QueryRequest(BaseModel):
  question: str

@app.on_event("startup")
def startup() -> None:
  global qa_chain
  qa_chain = build_qa()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
  UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
  dest = UPLOAD_DIR / file.filename
  dest.write_bytes(await file.read())
  n = ingest(dest)
  return {"status": "ok", "chunks": n}

@app.post("/query")
def query(req: QueryRequest):
  r = qa_chain({"query": req.question})
  sources = [d.metadata for d in r.get("source_documents", [])]
  return {"answer": r["result"], "sources": sources}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)
