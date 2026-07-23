#!/usr/bin/env python3
"""Day 40: LangChain ReAct Agent"""
import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

@tool
def get_weather(city: str) -> str:
  """查询城市天气"""
  return f"{city}：晴，25°C"

@tool
def kb_search(query: str) -> str:
  """搜索企业知识库"""
  return f"关于「{query}」：Nexus 支持 RAG 问答。"

llm = ChatOpenAI(
  model="deepseek-chat",
  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
tools = [get_weather, kb_search]
prompt = PromptTemplate.from_template("你有工具: {tools}\n问题: {input}\n{agent_scratchpad}")
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

if __name__ == "__main__":
  print(executor.invoke({"input": "北京天气怎么样？"}))
