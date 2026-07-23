#!/usr/bin/env python3
"""Day 40: AgentExecutor 配置与回调"""
from langchain.agents import AgentExecutor
from langchain_core.callbacks import BaseCallbackHandler

class LogHandler(BaseCallbackHandler):
  def on_tool_start(self, serialized, input_str, **kwargs):
    print(f"[TOOL] {serialized.get('name')} input={input_str}")

# 在 langchain_agent 中: AgentExecutor(..., callbacks=[LogHandler()])
