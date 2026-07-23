#!/usr/bin/env python3
"""Day 44: Agent 通过 MCP 调用工具"""
from mcp_server import handle_request

def mcp_tool(name: str, **kwargs) -> str:
  r = handle_request({"method": "tools/call", "params": {"name": name, **kwargs}})
  return r.get("content", str(r))

if __name__ == "__main__":
  print(mcp_tool("kb_search", query="报销流程"))
