#!/usr/bin/env python3
"""Day 47: SQL 安全守卫"""
FORBIDDEN = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", ";--"]

def is_safe_sql(sql: str) -> bool:
  upper = sql.upper()
  if not upper.strip().startswith("SELECT"):
    return False
  return not any(kw in upper for kw in FORBIDDEN)

if __name__ == "__main__":
  print(is_safe_sql("SELECT * FROM employees"))
  print(is_safe_sql("DROP TABLE employees"))
