#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""九九乘法表 — 嵌套 for 循环与格式化对齐。"""
SIZE = 9


def print_table(size: int = SIZE) -> None:
    for i in range(1, size + 1):
        parts: list[str] = []
        for j in range(1, i + 1):
            parts.append(f"{j}×{i}={i*j:2d}")
        print("  ".join(parts))


def main() -> None:
    print_table()


if __name__ == "__main__":
    main()
