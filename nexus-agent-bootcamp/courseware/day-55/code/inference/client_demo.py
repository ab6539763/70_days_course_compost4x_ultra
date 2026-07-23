#!/usr/bin/env python3
"""Day 55 — OpenAI 兼容 API 客户端演示"""
import json, os, urllib.request

def chat_completion(messages, base_url="http://localhost:8000/v1", mock=True):
    if mock:
        return f"[mock] {messages[-1]['content'][:40]}..."
    payload = json.dumps({"model": "nexus-agent", "messages": messages}).encode()
    req = urllib.request.Request(f"{base_url}/chat/completions", data=payload,
        headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print(chat_completion([{"role": "user", "content": "如何配置 RAG？"}]))
