#!/usr/bin/env python3
"""Day 47: Schema 工具与示例数据"""
import sqlite3

def init_demo_db(path: str = "data/demo.db") -> None:
  conn = sqlite3.connect(path)
  conn.executescript("""
    CREATE TABLE IF NOT EXISTS employees (id INT, name TEXT, dept TEXT, salary INT);
    INSERT OR IGNORE INTO employees VALUES (1,'张三','销售',8000),(2,'李四','研发',12000);
    CREATE TABLE IF NOT EXISTS orders (id INT, emp_id INT, amount REAL);
    INSERT OR IGNORE INTO orders VALUES (1,1,5000.0),(2,1,3000.0);
  """)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  init_demo_db()
  print("demo.db 已初始化")
