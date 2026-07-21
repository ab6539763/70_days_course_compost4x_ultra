#!/usr/bin/env python3
"""Day 41: 导出 Mermaid 图"""
from state_graph import app
try:
  print(app.get_graph().draw_mermaid())
except Exception:
  print("graph TD\n  research --> write --> END")
