#!/usr/bin/env python3
"""Scheduler Agent — 会议与日程安排"""
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Meeting:
  title: str
  start: datetime
  duration_min: int

class SchedulerAgent:
  def propose(self, title: str) -> Meeting:
    start = datetime.now() + timedelta(days=1)
    return Meeting(title=title, start=start, duration_min=60)

  def format_invite(self, m: Meeting) -> str:
    return f"会议邀请: {m.title} @ {m.start.isoformat()} ({m.duration_min}min)"
