#!/usr/bin/env python3
"""Day 46: 重试装饰器"""
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0):
  def deco(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      last_err = None
      for i in range(max_attempts):
        try:
          return fn(*args, **kwargs)
        except Exception as e:
          last_err = e
          time.sleep(delay * (i + 1))
      raise last_err
    return wrapper
  return deco

@retry(max_attempts=3)
def flaky_llm_call(prompt: str) -> str:
  import random
  if random.random() < 0.5:
    raise ConnectionError("timeout")
  return "ok"
