#!/usr/bin/env python3
"""Day 39: ReAct 工具集"""
import ast
import operator

def search(query: str) -> str:
  # 模拟搜索
  kb = {"Nexus RAG": "Nexus 使用 LangChain + Chroma 实现 RAG。"}
  for k, v in kb.items():
    if k.lower() in query.lower() or query.lower() in k.lower():
      return v
  return "未找到相关信息"

def calculator(expr: str) -> str:
  # 安全计算：仅允许数字与运算符
  allowed = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
  def _eval(node):
    if isinstance(node, ast.Num):
      return node.n
    if isinstance(node, ast.BinOp):
      return allowed[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError("非法表达式")
  try:
    return str(_eval(ast.parse(expr, mode="eval").body))
  except Exception as e:
    return f"计算错误: {e}"

TOOLS = {"search": search, "calculator": calculator}
