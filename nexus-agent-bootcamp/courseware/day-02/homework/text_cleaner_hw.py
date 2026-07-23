#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day 2 课后作业参考答案 — text_cleaner_hw.py
请先独立完成再对照！
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# 允许从 code/ 目录导入今日主模块
_CODE_DIR = Path(__file__).resolve().parent.parent / "code"
if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))

from text_cleaner import clean_text as base_clean_text  # noqa: E402


def mask_email(text: str) -> str:
    """将 user@domain.com 转为 u***@domain.com"""

    def repl(m: re.Match[str]) -> str:
        user, domain = m.group(1), m.group(2)
        masked = (user[0] + "***") if user else "***"
        return f"{masked}@{domain}"

    return re.sub(r"([\w.+-]+)@([\w.-]+\.\w+)", repl, text)


def extract_hashtags(text: str) -> list[str]:
    """返回所有 #话题，不含 # 号"""
    return re.findall(r"#([\w\u4e00-\u9fff]+)", text)


def clean_text_extended(raw: str) -> str:
    """在 base clean_text 基础上确保邮箱脱敏（作业要求）"""
    step = base_clean_text(raw)
    # base 已含 mask_email，此处演示可再调用
    step = mask_email(step)
    return step


def run_self_tests() -> None:
    """至少 3 个 assert 自测用例"""
    # 用例 1：话题提取
    tags = extract_hashtags("关注 #NexusAgent #大模型 和 #RAG")
    assert tags == ["NexusAgent", "大模型", "RAG"], f"话题提取失败: {tags}"

    # 用例 2：邮箱打码
    masked = mask_email("请联系 zhangming@smartlink.cn")
    assert "z***@smartlink.cn" in masked, f"邮箱打码失败: {masked}"

    # 用例 3：管道清洗保留语义
    result = clean_text_extended("  你好，世界！13812345678 zhang@ex.com  ")
    assert "138****5678" in result, f"手机打码失败: {result}"
    assert "z***@ex.com" in result, f"邮箱打码失败: {result}"
    assert "你好" in result, f"正文丢失: {result}"

    # 用例 4：空输入
    assert clean_text_extended("") == ""

    print("✅ 全部作业自测通过（4 个用例）")


def main() -> None:
    run_self_tests()
    sample = "#NexusAgent 好用！邮箱 dev@smartlink.cn 手机 13900001111"
    print(f"\n原始: {sample}")
    print(f"清洗: {clean_text_extended(sample)}")
    print(f"话题: {extract_hashtags(sample)}")


if __name__ == "__main__":
    main()
