#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易菜单系统 menu_system.py — Day 3 下午实操 S03
模拟 NexusAgent CLI 指令菜单雏形：字典 dispatch 替代长 elif 链

运行：
  python3 menu_system.py           # 交互模式
  python3 menu_system.py --test    # 自动化测试模式
"""
from __future__ import annotations

import argparse
import sys
from typing import Callable

# 类型别名：菜单处理函数
MenuHandler = Callable[[], None]

# 版本号 — 后续 Day 14 CLI 助手将沿用此模式
VERSION = "NexusAgent Bootcamp v0.1-day03"


def show_banner(print_fn: Callable[[str], None] = print) -> None:
    """打印程序横幅"""
    print_fn("=" * 44)
    print_fn("  NexusAgent CLI 菜单 (Day 3 教学版)")
    print_fn("=" * 44)


def show_menu(print_fn: Callable[[str], None] = print) -> None:
    """打印主菜单选项"""
    print_fn("1. 查看版本")
    print_fn("2. 查看今日学习目标")
    print_fn("3. 计算两数之和")
    print_fn("0. 退出")


def handle_version(print_fn: Callable[[str], None] = print) -> None:
    """菜单项 1：版本信息"""
    print_fn(VERSION)


def handle_goal(print_fn: Callable[[str], None] = print) -> None:
    """菜单项 2：学习目标"""
    print_fn("今日目标: 掌握 if/elif/else、while、for 与 break/continue")
    print_fn("明日预告: 列表与 todo_manager 待办系统")


def handle_add(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
) -> None:
    """菜单项 3：两数相加，含输入校验"""
    a = input_fn("输入整数 a: ").strip()
    b = input_fn("输入整数 b: ").strip()
    if not (a.lstrip("-").isdigit() and b.lstrip("-").isdigit()):
        print_fn("输入无效，请输入整数")
        return
    result = int(a) + int(b)
    print_fn(f"结果: {result}")


def build_actions(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
) -> dict[str, MenuHandler]:
    """构建菜单动作字典"""
    return {
        "1": lambda: handle_version(print_fn),
        "2": lambda: handle_goal(print_fn),
        "3": lambda: handle_add(input_fn, print_fn),
    }


def run_menu(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
    choices: list[str] | None = None,
) -> None:
    """
    主菜单循环 — while True + break 退出。

    Args:
        input_fn: 输入函数（测试时注入）
        print_fn: 输出函数
        choices: 预设选择序列（测试模式）；None 则交互输入
    """
    actions = build_actions(input_fn, print_fn)
    choice_iter = iter(choices) if choices else None
    invalid_count = 0
    max_invalid = 3

    show_banner(print_fn)
    while True:
        show_menu(print_fn)
        if choice_iter is not None:
            try:
                choice = next(choice_iter)
                print_fn(f"请选择: {choice}")
            except StopIteration:
                choice = "0"
                print_fn("请选择: 0")
        else:
            choice = input_fn("请选择: ").strip()

        # 退出分支 — break 跳出 while
        if choice == "0":
            print_fn("再见！")
            break

        handler = actions.get(choice)
        if handler is None:
            invalid_count += 1
            print_fn(f"无效选项，请重试（{invalid_count}/{max_invalid}）")
            if invalid_count >= max_invalid:
                print_fn("错误次数过多，返回主菜单并重置计数")
                invalid_count = 0
            continue

        invalid_count = 0  # 有效选择后重置
        handler()
        print_fn("-" * 44)


def run_test_mode() -> None:
    """自动化测试：模拟用户选择 1 → 3(10+20) → 0"""
    outputs: list[str] = []
    inputs = iter(["1", "3", "10", "20", "0"])

    def mock_input(prompt: str) -> str:
        value = next(inputs)
        outputs.append(f"{prompt}{value}")
        return value

    def mock_print(msg: str) -> None:
        outputs.append(msg)

    run_menu(input_fn=mock_input, print_fn=mock_print)
    combined = "\n".join(outputs)
    assert VERSION in combined, "应输出版本号"
    assert "30" in combined, "应输出 10+20=30"
    assert "再见" in combined, "应正常退出"
    print("=" * 44)
    print("  菜单系统 — 自动化测试模式")
    print("=" * 44)
    for line in outputs:
        print(line)
    print("=" * 44)
    print("✅ 菜单测试模式通过")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NexusAgent CLI 菜单 Day 3")
    parser.add_argument("--test", action="store_true", help="运行自动化测试")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.test:
            run_test_mode()
        else:
            run_menu()
    except KeyboardInterrupt:
        print("\n用户中断 (Ctrl+C)，安全退出")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
