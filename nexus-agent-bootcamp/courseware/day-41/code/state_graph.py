#!/usr/bin/env python3
"""Day 41: LangGraph StateGraph 入门"""
from typing import TypedDict
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
  messages: list[str]
  step: int

def research(state: AgentState) -> AgentState:
  state["messages"].append("检索: Nexus RAG 文档")
  state["step"] += 1
  return state

def write(state: AgentState) -> AgentState:
  state["messages"].append("生成: 基于检索的回答草稿")
  state["step"] += 1
  return state

graph = StateGraph(AgentState)
graph.add_node("research", research)
graph.add_node("write", write)
graph.set_entry_point("research")
graph.add_edge("research", "write")
graph.add_edge("write", END)
app = graph.compile()

if __name__ == "__main__":
  out = app.invoke({"messages": [], "step": 0})
  print(out)
