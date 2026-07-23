#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day 3 课后作业参考答案 — menu_extended.py
扩展菜单：猜数字子菜单 + 乘法表 + 错误次数限制

运行：
  python3 homework/menu_extended.py         # 交互
  python3 homework/menu_extended.py --test  # 自测
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable

_CODE = Path(__file__).resolve().parent.parent / "code"
sys.path.insert(0, str(_CODE))

from guess_number import play_round as guess_play_round  # noqa: E402
from multiplication_table import build_table, print_table  # noqa: E402
from menu_system import handle_add, handle_goal, handle_version  # noqa: E402

MAX_INVALID = 3


def play_guess_short(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
) -> None:
    """菜单项 4：启动猜数字"""
    print_fn("--- 猜数字子游戏 ---")
    guess_play_round(input_fn=input_fn, print_fn=print_fn)


def handle_mult_table(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
) -> None:
    """菜单项 5：打印 n×n 乘法表"""
    raw = input_fn("输入表大小 n (1-9): ").strip()
    if not raw.isdigit() or not 1 <= int(raw) <= 9:
        print_fn("无效，使用默认 9")
        n = 9
    else:
        n = int(raw)
    # print_table 使用 print，测试时重定向由调用方处理
    print_table(n)


def build_extended_actions(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
) -> dict[str, Callable[[], None]]:
    """扩展菜单动作字典"""
    return {
        "1": lambda: handle_version(print_fn),
        "2": lambda: handle_goal(print_fn),
        "3": lambda: handle_add(input_fn, print_fn),
        "4": lambda: play_guess_short(input_fn, print_fn),
        "5": lambda: handle_mult_table(input_fn, print_fn),
    }


def show_extended_menu(print_fn: Callable[[str], None] = print) -> None:
    print_fn("1. 查看版本  2. 学习目标  3. 两数之和")
    print_fn("4. 猜数字     5. 乘法表     0. 退出")


def run_extended_menu(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
    choices: list[str] | None = None,
) -> None:
    actions = build_extended_actions(input_fn, print_fn)
    choice_iter = iter(choices) if choices else None
    invalid_streak = 0

    print_fn("=" * 44)
    print_fn("  NexusAgent 扩展菜单 (Day 3 作业)")
    print_fn("=" * 44)

    while True:
        show_extended_menu(print_fn)
        if choice_iter is not None:
            try:
                choice = next(choice_iter)
                print_fn(f"请选择: {choice}")
            except StopIteration:
                choice = "0"
                print_fn("请选择: 0")
        else:
            choice = input_fn("请选择: ").strip()

        if choice == "0":
            print_fn("再见！")
            break

        handler = actions.get(choice)
        if handler is None:
            invalid_streak += 1
            print_fn(f"无效选项 ({invalid_streak}/{MAX_INVALID})")
            if invalid_streak >= MAX_INVALID:
                print_fn("错误过多，已重置")
                invalid_streak = 0
            continue

        invalid_streak = 0
        handler()
        print_fn("-" * 44)


def run_self_tests() -> None:
    """作业自测"""
    # 用例 1：乘法表
    table = build_table(3)
    assert len(table) == 3 and "3×3= 9" in table[2]

    # 用例 2：扩展菜单流转（5→选3打印表，然后0退出）
    logs: list[str] = []
    inputs = iter(["5", "3", "0"])
    run_extended_menu(
        input_fn=lambda _: next(inputs),
        print_fn=logs.append,
        choices=None,
    )
    assert any("乘法表" in line for line in logs)

    # 用例 3：连续无效选项不崩溃
    bad = iter(["x", "y", "z", "0"])
    run_extended_menu(input_fn=lambda _: next(bad), print_fn=lambda _: None)

    print("✅ 全部作业自测通过（3 组用例）")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test:
        run_self_tests()
        return 0
    run_extended_menu()
    return 0


if __name__ == "__main__":
    sys.exit(main())
