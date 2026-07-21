#!/usr/bin/env python3
"""LangGraph 工作流 — Supervisor 调度多 Agent"""
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from agents.scheduler import SchedulerAgent

class OfficeState(TypedDict):
  task: str
  route: str
  context: str
  output: str

researcher = ResearcherAgent()
writer = WriterAgent()
scheduler = SchedulerAgent()

def supervisor(state: OfficeState) -> OfficeState:
  t = state["task"]
  if "会议" in t or "日程" in t:
    state["route"] = "scheduler"
  elif "写" in t or "邮件" in t or "报告" in t:
    state["route"] = "writer"
  else:
    state["route"] = "researcher"
  return state

def run_researcher(state: OfficeState) -> OfficeState:
  r = researcher.run(state["task"])
  state["context"] = "\n".join(r.findings)
  state["output"] = state["context"]
  return state

def run_writer(state: OfficeState) -> OfficeState:
  if not state.get("context"):
    run_researcher(state)
  d = writer.run(state["task"], state["context"])
  state["output"] = d.body
  return state

def run_scheduler(state: OfficeState) -> OfficeState:
  m = scheduler.propose(state["task"])
  state["output"] = scheduler.format_invite(m)
  return state

def route(state: OfficeState) -> Literal["researcher", "writer", "scheduler"]:
  return state["route"]

def build_graph():
  g = StateGraph(OfficeState)
  g.add_node("supervisor", supervisor)
  g.add_node("researcher", run_researcher)
  g.add_node("writer", run_writer)
  g.add_node("scheduler", run_scheduler)
  g.set_entry_point("supervisor")
  g.add_conditional_edges("supervisor", route, {
    "researcher": "researcher", "writer": "writer", "scheduler": "scheduler"
  })
  g.add_edge("researcher", END)
  g.add_edge("writer", END)
  g.add_edge("scheduler", END)
  return g.compile()

if __name__ == "__main__":
  app = build_graph()
  for task in ["查询年假政策", "写一封项目周报邮件", "安排下周评审会议"]:
    print(task, "->", app.invoke({"task": task, "route": "", "context": "", "output": ""})["output"][:80])
