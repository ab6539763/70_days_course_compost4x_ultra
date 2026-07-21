#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验工具 — 从菜单系统中抽离的输入验证逻辑。"""
from __future__ import annotations


def is_int_string(value: str) -> bool:
    value = value.strip()
    if value.startswith("-"):
        return value[1:].isdigit() if len(value) > 1 else False
    return value.isdigit()


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def require_non_empty(value: str, field_name: str = "字段") -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name}不能为空")
    return cleaned
