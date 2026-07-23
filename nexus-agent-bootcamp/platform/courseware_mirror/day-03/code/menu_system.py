#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易菜单系统 — 流程控制综合练习
模拟 NexusAgent CLI 指令菜单雏形
"""
from __future__ import annotations

import sys


def show_banner() -> None:
    print("=" * 40)
    print("  NexusAgent CLI 菜单 (Day 3 教学版)")
    print("=" * 40)


def show_menu() -> None:
    print("1. 查看版本")
    print("2. 查看今日学习目标")
    print("3. 计算两数之和")
    print("0. 退出")


def handle_version() -> None:
    print("NexusAgent Bootcamp v0.1-day03")


def handle_goal() -> None:
    print("今日目标: 掌握 if/elif/else、while、for 与 break/continue")


def handle_add() -> None:
    a = input("输入整数 a: ").strip()
    b = input("输入整数 b: ").strip()
    if not (a.lstrip("-").isdigit() and b.lstrip("-").isdigit()):
        print("输入无效，请输入整数")
        return
    result = int(a) + int(b)
    print(f"结果: {result}")


def run_menu() -> None:
    actions = {
        "1": handle_version,
        "2": handle_goal,
        "3": handle_add,
    }
    show_banner()
    while True:
        show_menu()
        choice = input("请选择: ").strip()
        if choice == "0":
            print("再见！")
            break
        handler = actions.get(choice)
        if handler is None:
            print("无效选项，请重试")
            continue
        handler()
        print("-" * 40)


def main() -> None:
    try:
        run_menu()
    except KeyboardInterrupt:
        print("\n用户中断，安全退出")
        sys.exit(0)


if __name__ == "__main__":
    main()
