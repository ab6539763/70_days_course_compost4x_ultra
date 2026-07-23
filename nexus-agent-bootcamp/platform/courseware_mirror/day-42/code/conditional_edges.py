#!/usr/bin/env python3
"""Day 42: 条件路由"""
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

class State(TypedDict):
  query: str
  route: str
  answer: str

def classify(state: State) -> State:
  state["route"] = "kb" if "政策" in state["query"] or "年假" in state["query"] else "general"
  return state

def kb_node(state: State) -> State:
  state["answer"] = "知识库回答: 年假5天"
  return state

def general_node(state: State) -> State:
  state["answer"] = "通用回答: 请问具体需求"
  return state

def route_fn(state: State) -> Literal["kb", "general"]:
  return state["route"]

g = StateGraph(State)
g.add_node("classify", classify)
g.add_node("kb", kb_node)
g.add_node("general", general_node)
g.set_entry_point("classify")
g.add_conditional_edges("classify", route_fn, {"kb": "kb", "general": "general"})
g.add_edge("kb", END)
g.add_edge("general", END)
app = g.compile()

if __name__ == "__main__":
  print(app.invoke({"query": "年假政策", "route": "", "answer": ""}))
