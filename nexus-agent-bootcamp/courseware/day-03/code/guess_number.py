#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猜数字游戏 guess_number.py — Day 3 下午实操 S01
练习：while、if/elif/else、break、continue、random、输入校验

运行：
  python3 guess_number.py           # 交互模式
  python3 guess_number.py --demo    # 演示模式（自动化，供测试）
"""
from __future__ import annotations

import argparse
import random
import sys
from typing import Callable

# 游戏配置常量 — 全大写表示不可变配置
SECRET_MIN = 1
SECRET_MAX = 100
MAX_ATTEMPTS = 7


def compare_guess(guess: int, target: int) -> str:
    """
    比较猜测值与目标值，返回结果标识。
    纯函数，便于单元测试，不依赖 input/print。

    Returns:
        "low" | "high" | "win"
    """
    if guess < target:
        return "low"
    if guess > target:
        return "high"
    return "win"


def is_valid_guess_input(raw: str) -> bool:
    """校验用户输入是否为合法正整数（在范围内）。"""
    raw = raw.strip()
    if not raw.isdigit():
        return False
    value = int(raw)
    return SECRET_MIN <= value <= SECRET_MAX


def play_round(
    *,
    target: int | None = None,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
    max_attempts: int = MAX_ATTEMPTS,
) -> bool:
    """
    进行一局猜数字游戏。

    Args:
        target: 指定目标数（测试用）；None 则随机生成
        input_fn: 输入函数（测试时可注入 mock）
        print_fn: 输出函数
        max_attempts: 最大尝试次数

    Returns:
        True 猜中，False 次数用尽
    """
    secret = target if target is not None else random.randint(SECRET_MIN, SECRET_MAX)
    print_fn(
        f"我想了一个 {SECRET_MIN}-{SECRET_MAX} 的整数，你有 {max_attempts} 次机会。"
    )

    attempts = 0
    # while 循环：次数未用尽则继续
    while attempts < max_attempts:
        attempts += 1
        raw = input_fn(f"第 {attempts} 次猜测: ")

        # 输入校验失败：不消耗次数（attempts 回退）+ continue 跳过本轮
        if not is_valid_guess_input(raw):
            print_fn(f"请输入 {SECRET_MIN}-{SECRET_MAX} 之间的有效整数！")
            attempts -= 1
            continue

        guess = int(raw.strip())
        result = compare_guess(guess, secret)

        if result == "low":
            print_fn("太小了 ↑")
        elif result == "high":
            print_fn("太大了 ↓")
        else:
            print_fn(f"🎉 恭喜！{attempts} 次猜中！答案是 {secret}")
            return True

    print_fn(f"游戏结束，次数用尽。答案是 {secret}")
    return False


def run_demo() -> None:
    """演示模式：固定目标 42，脚本化输入，供 CI/全链路测试"""
    scripted_inputs = iter(["20", "60", "45", "42"])
    target = 42

    def mock_input(prompt: str) -> str:
        value = next(scripted_inputs)
        print(f"{prompt}{value}")
        return value

    print("=" * 50)
    print("  猜数字游戏 — 演示模式（目标=42）")
    print("=" * 50)
    won = play_round(target=target, input_fn=mock_input, print_fn=print)
    assert won, "演示模式应猜中"
    print("✅ 演示模式完成")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="猜数字游戏 Day 3")
    parser.add_argument("--demo", action="store_true", help="运行自动化演示")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.demo:
        run_demo()
        return 0
    play_round()
    return 0


if __name__ == "__main__":
    sys.exit(main())
