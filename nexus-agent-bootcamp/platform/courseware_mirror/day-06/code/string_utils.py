#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""字符串工具模块 — 供重构演示的原始实现片段。"""
from __future__ import annotations

import re


def is_blank(text: str) -> bool:
    return text.strip() == ""


def truncate(text: str, max_len: int, suffix: str = "...") -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")
