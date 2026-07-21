#!/usr/bin/env python3
"""Day 47: Text2SQL Agent"""
import os
import sqlite3
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

SCHEMA = """
CREATE TABLE employees (id INT, name TEXT, dept TEXT, salary INT);
CREATE TABLE orders (id INT, emp_id INT, amount REAL, created_at TEXT);
"""

prompt = ChatPromptTemplate.from_template(
  "根据 Schema 将问题转为 SQLite SQL，只输出 SQL。\nSchema:\n{schema}\n问题:{question}"
)
llm = ChatOpenAI(
  model="deepseek-chat",
  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)

def generate_sql(question: str) -> str:
  r = (prompt | llm).invoke({"schema": SCHEMA, "question": question})
  return r.content.strip().strip("`").replace("sql\n", "")

def run_sql(sql: str, db: str = ":memory:") -> list:
  # 安全：仅允许 SELECT
  if not sql.strip().upper().startswith("SELECT"):
    raise ValueError("仅允许 SELECT 查询")
  conn = sqlite3.connect(db)
  cur = conn.execute(sql)
  rows = cur.fetchall()
  conn.close()
  return rows

if __name__ == "__main__":
  q = "查询销售部员工数量"
  sql = generate_sql(q) if os.getenv("DEEPSEEK_API_KEY") else "SELECT COUNT(*) FROM employees WHERE dept='销售'"
  print("SQL:", sql)
