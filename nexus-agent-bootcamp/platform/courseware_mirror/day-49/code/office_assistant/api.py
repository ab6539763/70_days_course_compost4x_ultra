#!/usr/bin/env python3
"""办公助手 FastAPI 服务"""
from fastapi import FastAPI
from pydantic import BaseModel
from graph.workflow import build_graph

app = FastAPI(title="Nexus Office Assistant")
workflow = build_graph()

class TaskRequest(BaseModel):
  task: str

@app.post("/assist")
def assist(req: TaskRequest):
  r = workflow.invoke({"task": req.task, "route": "", "context": "", "output": ""})
  return {"output": r["output"], "route": r["route"]}
