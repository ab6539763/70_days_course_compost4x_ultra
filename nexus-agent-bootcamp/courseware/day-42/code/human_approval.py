#!/usr/bin/env python3
"""Day 42: 人工审批节点（概念）"""
from typing import TypedDict

class State(TypedDict):
  draft: str
  approved: bool

def generate_draft(state: State) -> State:
  state["draft"] = "待审批的邮件草稿..."
  return state

def wait_approval(state: State) -> State:
  # 生产环境对接审批 API；教学用 input 模拟
  ans = input("批准此草稿? y/n: ")
  state["approved"] = ans.lower() == "y"
  return state
