#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
函数与重构综合演示 refactor_demo.py
展示：抽取函数、默认参数、*args/**kwargs、文档字符串
"""
from __future__ import annotations

from typing import Any, Callable

from string_utils import is_blank, slugify, truncate
from validators import clamp, is_int_string, require_non_empty


def greet(name: str, title: str = "同学") -> str:
    """生成问候语；title 为默认参数。"""
    safe_name = require_non_empty(name, "姓名")
    return f"你好，{title} {safe_name}！欢迎回到 NexusAgent 训练营。"


def apply_ops(values: list[int], *ops: Callable[[int], int]) -> list[int]:
    """对列表每个元素依次应用多个一元函数。"""
    result = list(values)
    for op in ops:
        result = [op(x) for x in result]
    return result


def build_user_record(**fields: Any) -> dict[str, Any]:
    """使用 **kwargs 构建用户记录字典。"""
    record = {"source": "bootcamp"}
    record.update(fields)
    return record


def format_profile(name: str, bio: str, max_bio: int = 80) -> str:
    """组合多个工具函数格式化个人简介。"""
    if is_blank(bio):
        bio = "（暂无简介）"
    short_bio = truncate(bio, max_bio)
    slug = slugify(name)
    return f"用户: {name} | slug: {slug} | 简介: {short_bio}"


def parse_menu_number(raw: str, low: int = 0, high: int = 9) -> int | None:
    """解析菜单数字输入，非法返回 None。"""
    if not is_int_string(raw):
        return None
    num = int(raw.strip())
    return clamp(num, low, high)


def demo() -> None:
    print(greet("张晓明"))
    print(greet("李雷", title="工程师"))
    doubled = apply_ops([1, 2, 3], lambda x: x * 2, lambda x: x + 1)
    print("apply_ops:", doubled)
    user = build_user_record(name="小王", role="学员", day=6)
    print("user record:", user)
    print(format_profile("Nexus Agent", "企业级智能体平台" * 5))
    print("menu parse:", parse_menu_number("42", 0, 9))


def main() -> None:
    demo()


if __name__ == "__main__":
    main()
