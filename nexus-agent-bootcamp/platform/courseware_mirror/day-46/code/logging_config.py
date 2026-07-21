#!/usr/bin/env python3
"""Day 46: 结构化日志"""
import json
import logging
from datetime import datetime

class JsonFormatter(logging.Formatter):
  def format(self, record: logging.LogRecord) -> str:
    return json.dumps({
      "ts": datetime.utcnow().isoformat(),
      "level": record.levelname,
      "msg": record.getMessage(),
      "module": record.module,
    }, ensure_ascii=False)

def setup_logging() -> None:
  h = logging.StreamHandler()
  h.setFormatter(JsonFormatter())
  logging.getLogger().handlers = [h]
  logging.getLogger().setLevel(logging.INFO)
