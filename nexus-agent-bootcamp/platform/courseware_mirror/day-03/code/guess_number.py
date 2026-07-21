#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""猜数字游戏 — 练习 while、if、break 与随机数。"""
import random

SECRET_MIN = 1
SECRET_MAX = 100
MAX_ATTEMPTS = 7


def play_round() -> None:
    target = random.randint(SECRET_MIN, SECRET_MAX)
    attempts = 0
    print(f"我想了一个 {SECRET_MIN}-{SECRET_MAX} 的整数，你有 {MAX_ATTEMPTS} 次机会。")
    while attempts < MAX_ATTEMPTS:
        attempts += 1
        raw = input(f"第 {attempts} 次猜测: ").strip()
        if not raw.isdigit():
            print("请输入有效数字！")
            attempts -= 1
            continue
        guess = int(raw)
        if guess < target:
            print("太小了 ↑")
        elif guess > target:
            print("太大了 ↓")
        else:
            print(f"恭喜！{attempts} 次猜中！")
            return
    print(f"游戏结束，答案是 {target}")


def main() -> None:
    play_round()


if __name__ == "__main__":
    main()
