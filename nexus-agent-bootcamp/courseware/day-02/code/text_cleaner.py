#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本清洗工具 text_cleaner.py — Day 2 下午核心交付
企业场景：客服工单、用户评论入库前的标准化预处理
Jira: NEXUS-E1-D02-S01 / NEXUS-E1-D02-S02

运行方式：
  python3 text_cleaner.py              # 演示模式
  python3 text_cleaner.py --file ../assets/sample_comments.txt
  python3 text_cleaner.py --stdin      # 从标准输入读取
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from typing import Iterable

# 定义默认需要剥离的空白字符集合
WHITESPACE_CHARS = " \t\n\r\f\v"

# 定义常见中文标点映射表（全角 -> 半角或统一形式）
PUNCT_MAP = {
    "，": ",",
    "。": ".",
    "！": "!",
    "？": "?",
    "：": ":",
    "；": ";",
    "（": "(",
    "）": ")",
    "【": "[",
    "】": "]",
}


def normalize_unicode(text: str) -> str:
    """将文本做 NFKC 规范化，全角字母数字转半角。"""
    return unicodedata.normalize("NFKC", text)


def strip_edges(text: str) -> str:
    """去除首尾空白字符。"""
    return text.strip(WHITESPACE_CHARS)


def collapse_internal_spaces(text: str) -> str:
    """将连续空白压缩为单个空格。"""
    return re.sub(r"\s+", " ", text)


def replace_punctuation(text: str, mapping: dict[str, str] | None = None) -> str:
    """按映射表替换标点符号。"""
    table = mapping if mapping is not None else PUNCT_MAP
    result = text
    for src, dst in table.items():
        result = result.replace(src, dst)
    return result


def remove_urls(text: str) -> str:
    """将 http/https 链接替换为占位符 [URL]。"""
    pattern = r"https?://\S+"
    return re.sub(pattern, "[URL]", text)


def remove_mentions(text: str) -> str:
    """将 @用户名 替换为 @USER（不触碰邮箱中的 @）。"""
    # (?<!\w) 确保 @ 前不是字母数字，避免误伤 user@domain.com
    pattern = r"(?<!\w)@\w+"
    return re.sub(pattern, "@USER", text)


def mask_phone_numbers(text: str) -> str:
    """中国大陆 11 位手机号打码：保留前 3 后 4。"""

    def _mask(match: re.Match[str]) -> str:
        phone = match.group(0)
        if len(phone) < 7:
            return phone
        return phone[:3] + "****" + phone[-4:]

    return re.sub(r"1\d{10}", _mask, text)


def mask_email(text: str) -> str:
    """
    邮箱脱敏：zhangming@smartlink.cn → z***@smartlink.cn
    作业扩展功能，已集成进主管道。
    """

    def _repl(match: re.Match[str]) -> str:
        user, domain = match.group(1), match.group(2)
        if not user:
            return f"***@{domain}"
        masked_user = user[0] + "***" if len(user) >= 1 else "***"
        return f"{masked_user}@{domain}"

    return re.sub(r"([\w.+-]+)@([\w.-]+\.\w+)", _repl, text)


def extract_hashtags(text: str) -> list[str]:
    """提取 #话题 标签，返回不含 # 的列表。支持中英文。"""
    return re.findall(r"#([\w\u4e00-\u9fff]+)", text)


def clean_text(
    raw: str,
    *,
    mask_phone: bool = True,
    mask_email_flag: bool = True,
) -> str:
    """
    管道式清洗：按固定顺序应用各子步骤。
    mask_phone / mask_email_flag 为关键字-only 参数。
    """
    if not raw:
        return ""
    step = normalize_unicode(raw)
    step = strip_edges(step)
    step = collapse_internal_spaces(step)
    step = replace_punctuation(step)
    step = remove_urls(step)
    step = remove_mentions(step)
    if mask_phone:
        step = mask_phone_numbers(step)
    if mask_email_flag:
        step = mask_email(step)
    return step


def batch_clean(lines: Iterable[str], **kwargs: object) -> list[str]:
    """批量清洗多行文本。"""
    return [clean_text(line, **kwargs) for line in lines]  # type: ignore[arg-type]


def word_count(text: str) -> dict[str, int]:
    """统计字符数、词数（空白分词）、行数。"""
    return {
        "chars": len(text),
        "words": len(text.split()) if text else 0,
        "lines": len(text.splitlines()) if text else 0,
    }


def is_palindrome(s: str) -> bool:
    """
    判断是否为回文字符串（忽略大小写与非字母数字）
    晚自习 LeetCode 风格练习
    """
    cleaned = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]", "", s).lower()
    return cleaned == cleaned[::-1] and len(cleaned) > 0


def process_file(path: Path) -> list[str]:
    """从文件读取并批量清洗，UTF-8 编码。"""
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    return batch_clean(lines)


def demo() -> None:
    """演示入口：构造脏数据并打印清洗前后对比。"""
    dirty_samples = [
        "  你好，世界！  访问 https://smartlink.cn/docs  ",
        "@alice 我的手机号是13812345678，请回电。邮箱 zhangming@smartlink.cn",
        "全角ＡＢＣ１２３　测试 #NexusAgent #大模型",
        "联系 support@example.com 或 13900001111",
    ]
    print("=" * 60)
    print("  text_cleaner 演示 — 智链科技 NexusAgent Day 2")
    print("=" * 60)
    for idx, raw in enumerate(dirty_samples, start=1):
        cleaned = clean_text(raw)
        tags = extract_hashtags(raw)
        stats = word_count(cleaned)
        print(f"[样本 {idx}] 原始: {raw!r}")
        print(f"[样本 {idx}] 清洗: {cleaned!r}")
        if tags:
            print(f"[样本 {idx}] 话题: {tags}")
        print(f"[样本 {idx}] 统计: {stats}")
        print("-" * 60)
    # 回文练习
    palindrome_cases = ["A man a plan a canal Panama", "上海自来水来自海上", "hello"]
    print("【回文检测练习】")
    for p in palindrome_cases:
        print(f"  {p!r} → {is_palindrome(p)}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="NexusAgent 文本清洗工具 Day 2")
    parser.add_argument("--file", "-f", type=Path, help="从文件批量清洗（每行一条）")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取")
    parser.add_argument("--demo", action="store_true", help="运行内置演示（默认）")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """主入口，返回进程退出码。"""
    args = parse_args(argv)

    if args.file:
        try:
            results = process_file(args.file)
        except FileNotFoundError as e:
            print(f"错误: {e}", file=sys.stderr)
            return 1
        for i, line in enumerate(results, 1):
            print(f"{i:03d}| {line}")
        print(f"\n✅ 已清洗 {len(results)} 行")
        return 0

    if args.stdin:
        lines = sys.stdin.read().splitlines()
        for line in batch_clean(lines):
            print(line)
        return 0

    # 默认演示
    demo()
    return 0


if __name__ == "__main__":
    sys.exit(main())
