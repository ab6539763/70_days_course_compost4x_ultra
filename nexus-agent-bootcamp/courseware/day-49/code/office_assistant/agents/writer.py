#!/usr/bin/env python3
"""Writer Agent — 文档与邮件撰写"""
from dataclasses import dataclass

@dataclass
class Draft:
  title: str
  body: str

class WriterAgent:
  def run(self, task: str, context: str) -> Draft:
    body = f"根据以下资料撰写:\n{context}\n\n---\n{task} 的回复草稿..."
    return Draft(title=task[:30], body=body)
