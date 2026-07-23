#!/usr/bin/env python3
"""Day 57 — 审计日志模块"""
import json, hashlib
from datetime import datetime, timezone
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir=Path("logs/audit")):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_event(self, event_type, user_id, details):
        record = {"ts": datetime.now(timezone.utc).isoformat(), "type": event_type,
                  "user": user_id, "details": details}
        f = self.log_dir / f"audit_{datetime.now(timezone.utc):%Y%m%d}.jsonl"
        f.open("a").write(json.dumps(record, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    AuditLogger().log_event("llm_inference", "u001", {"model": "nexus-agent"})
    print("审计日志已写入")
