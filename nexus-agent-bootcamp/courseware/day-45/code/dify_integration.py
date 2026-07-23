#!/usr/bin/env python3
"""Day 45: Dify API 对接"""
import os
import json
import urllib.request

DIFY_API = os.getenv("DIFY_API_BASE", "https://api.dify.ai/v1")
DIFY_KEY = os.getenv("DIFY_API_KEY", "")

def chat(message: str, user: str = "nexus-user") -> str:
  if not DIFY_KEY:
    return f"[MOCK Dify] 回复: {message[:50]}..."
  payload = {"inputs": {}, "query": message, "user": user, "response_mode": "blocking"}
  req = urllib.request.Request(
    f"{DIFY_API}/chat-messages",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {DIFY_KEY}", "Content-Type": "application/json"},
    method="POST",
  )
  with urllib.request.urlopen(req, timeout=60) as resp:
    return json.loads(resp.read())["answer"]

if __name__ == "__main__":
  print(chat("Nexus 平台有哪些功能？"))
