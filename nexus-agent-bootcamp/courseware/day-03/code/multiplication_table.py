#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
九九乘法表 multiplication_table.py — Day 3 下午实操 S02
练习：嵌套 for 循环、f-string 格式化对齐、range()

运行：
  python3 multiplication_table.py           # 默认 9×9
  python3 multiplication_table.py --size 5  # 5×5
"""
from __future__ import annotations

import argparse
import sys

# 默认表大小
DEFAULT_SIZE = 9
MIN_SIZE = 1
MAX_SIZE = 9


def build_row(i: int) -> str:
    """
    构建乘法表第 i 行（1-indexed）。
    例如 i=3 → "1×3= 3  2×3= 6  3×3= 9"
    """
    parts: list[str] = []
    # 内层 for：j 从 1 到 i（三角形左下半部分）
    for j in range(1, i + 1):
        # :2d 右对齐两位整数，保持列对齐
        parts.append(f"{j}×{i}={i * j:2d}")
    return "  ".join(parts)


def build_table(size: int = DEFAULT_SIZE) -> list[str]:
    """
    生成完整乘法表行列表（纯函数，便于测试）。

    Args:
        size: 表边长，1-9

    Returns:
        每行一个字符串的列表
    """
    if not MIN_SIZE <= size <= MAX_SIZE:
        raise ValueError(f"size 必须在 {MIN_SIZE}-{MAX_SIZE} 之间，收到: {size}")
    rows: list[str] = []
    # 外层 for：控制行号 i
    for i in range(1, size + 1):
        rows.append(build_row(i))
    return rows


def print_table(size: int = DEFAULT_SIZE) -> None:
    """打印乘法表到标准输出"""
    print("=" * 50)
    print(f"  {size}×{size} 乘法表 — Day 3")
    print("=" * 50)
    for row in build_table(size):
        print(row)
    print("=" * 50)
    print("✅ multiplication_table 运行成功")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="九九乘法表 Day 3")
    parser.add_argument(
        "--size", "-n",
        type=int,
        default=DEFAULT_SIZE,
        help=f"表大小 ({MIN_SIZE}-{MAX_SIZE})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        print_table(args.size)
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
