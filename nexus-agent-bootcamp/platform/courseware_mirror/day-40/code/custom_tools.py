#!/usr/bin/env python3
"""Day 40: 自定义 Tool"""
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class CalcInput(BaseModel):
  expression: str = Field(description="数学表达式")

def calc(expression: str) -> str:
  return str(eval(expression))  # 教学简化，生产需沙箱

calc_tool = StructuredTool.from_function(func=calc, name="calculator", description="计算表达式", args_schema=CalcInput)
