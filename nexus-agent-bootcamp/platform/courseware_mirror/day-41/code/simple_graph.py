#!/usr/bin/env python3
"""Day 41: 消息列表状态"""
from langgraph.graph import MessagesState, StateGraph, END

def chatbot(state: MessagesState):
  return {"messages": state["messages"] + [{"role": "assistant", "content": "收到"}]}

g = StateGraph(MessagesState)
g.add_node("bot", chatbot)
g.set_entry_point("bot")
g.add_edge("bot", END)
app = g.compile()
