#!/usr/bin/env python3
"""Day 44: 简易 MCP Server（教学 mock）"""
import json
from typing import Any

TOOLS = {
  "kb_search": {"description": "搜索知识库", "params": {"query": "string"}},
  "get_time": {"description": "获取当前时间", "params": {}},
}

def handle_request(req: dict[str, Any]) -> dict[str, Any]:
  method = req.get("method")
  if method == "tools/list":
    return {"tools": [{"name": k, **v} for k, v in TOOLS.items()]}
  if method == "tools/call":
    name = req["params"]["name"]
    if name == "kb_search":
      return {"content": f"检索结果: {req['params'].get('query')}"}
    if name == "get_time":
      import datetime
      return {"content": datetime.datetime.now().isoformat()}
  return {"error": "unknown method"}

if __name__ == "__main__":
  sample = {"method": "tools/call", "params": {"name": "kb_search", "query": "年假"}}
  print(json.dumps(handle_request(sample), ensure_ascii=False))
