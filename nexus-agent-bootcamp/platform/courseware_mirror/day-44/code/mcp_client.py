#!/usr/bin/env python3
"""Day 44: MCP Client 调用 Server"""
import json
import subprocess

class MCPClient:
  def __init__(self, server_cmd: list[str]):
    self.proc = subprocess.Popen(server_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

  def call(self, method: str, params: dict | None = None) -> dict:
    req = {"method": method, "params": params or {}}
    self.proc.stdin.write(json.dumps(req) + "\n")
    self.proc.stdin.flush()
    line = self.proc.stdout.readline()
    return json.loads(line) if line else {}

# 教学：直接 import server 演示
from mcp_server import handle_request

if __name__ == "__main__":
  print(handle_request({"method": "tools/list"}))
