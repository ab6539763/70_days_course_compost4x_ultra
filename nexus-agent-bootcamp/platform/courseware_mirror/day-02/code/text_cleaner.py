#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本清洗工具 text_cleaner.py
企业场景：客服工单、用户评论入库前的标准化预处理
"""

# 导入 re 模块，提供正则表达式能力
import re

# 导入 unicodedata，用于 Unicode 规范化（全角转半角等）
import unicodedata

# 导入 typing 中的类型别名辅助（仅注解，运行时不强制）
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
    """将文本做 NFC 规范化，减少同形异码问题。"""
    # NFKC 兼容分解再组合，常用于全角字母数字
    return unicodedata.normalize("NFKC", text)


def strip_edges(text: str) -> str:
    """去除首尾空白字符。"""
    # str.strip 可传入自定义字符集
    return text.strip(WHITESPACE_CHARS)


def collapse_internal_spaces(text: str) -> str:
    """将连续空白压缩为单个空格。"""
    # 正则 \s+ 匹配任意空白 run
    return re.sub(r"\s+", " ", text)


def replace_punctuation(text: str, mapping: dict[str, str] | None = None) -> str:
    """按映射表替换标点符号。"""
    # 若未传入映射则使用模块级默认表
    table = mapping if mapping is not None else PUNCT_MAP
    # 遍历映射逐项 replace（数据量小，Day2 足够）
    result = text
    for src, dst in table.items():
        result = result.replace(src, dst)
    return result


def remove_urls(text: str) -> str:
    """删除 http/https 链接，防止垃圾信息入库。"""
    # 简单 URL 正则，教学用途不追求 RFC 完整覆盖
    pattern = r"https?://\S+"
    return re.sub(pattern, "[URL]", text)


def remove_mentions(text: str) -> str:
    """将 @用户名 替换为占位符。"""
    pattern = r"@\w+"
    return re.sub(pattern, "@USER", text)


def mask_phone_numbers(text: str) -> str:
    """中国大陆手机号打码：保留前3后4。"""
    def _mask(match: re.Match[str]) -> str:
        # 提取匹配到的完整号码字符串
        phone = match.group(0)
        # 长度不足则原样返回
        if len(phone) < 7:
            return phone
        # 中间四位替换为星号
        return phone[:3] + "****" + phone[-4:]
    # 匹配 11 位 1 开头手机号
    return re.sub(r"1\d{10}", _mask, text)


def clean_text(raw: str, *, mask_phone: bool = True) -> str:
    """
    管道式清洗：按固定顺序应用各子步骤。
    mask_phone 为关键字-only 参数，调用时必须写参数名。
    """
    # 空输入直接返回空串，避免后续无意义计算
    if not raw:
        return ""
    # 步骤 1：Unicode 规范化
    step = normalize_unicode(raw)
    # 步骤 2：去首尾空白
    step = strip_edges(step)
    # 步骤 3：压缩内部空白
    step = collapse_internal_spaces(step)
    # 步骤 4：标点统一
    step = replace_punctuation(step)
    # 步骤 5：URL 与 @ 处理
    step = remove_urls(step)
    step = remove_mentions(step)
    # 步骤 6：可选手机号脱敏
    if mask_phone:
        step = mask_phone_numbers(step)
    return step


def batch_clean(lines: Iterable[str]) -> list[str]:
    """批量清洗多行文本，返回新列表。"""
    # 列表推导式对每行调用 clean_text
    return [clean_text(line) for line in lines]


def word_count(text: str) -> dict[str, int]:
    """统计字符数、词数（空白分词）、行数。"""
    # 字符总数含标点
    chars = len(text)
    # split 默认按任意空白切分
    words = len(text.split()) if text else 0
    # 按换行分段
    lines = len(text.splitlines()) if text else 0
    # 返回结构化统计字典
    return {"chars": chars, "words": words, "lines": lines}


def demo() -> None:
    """演示入口：构造脏数据并打印清洗前后对比。"""
    dirty_samples = [
        "  你好，世界！  访问 https://smartlink.cn/docs  ",
        "@alice 我的手机号是13812345678，请回电。",
        "全角ＡＢＣ１２３　测试",
    ]
    print("=" * 56)
    print("text_cleaner 演示")
    print("=" * 56)
    for idx, raw in enumerate(dirty_samples, start=1):
        cleaned = clean_text(raw)
        stats = word_count(cleaned)
        print(f"[样本 {idx}] 原始: {raw!r}")
        print(f"[样本 {idx}] 清洗: {cleaned!r}")
        print(f"[样本 {idx}] 统计: {stats}")
        print("-" * 56)


def main() -> None:
    demo()


if __name__ == "__main__":
    main()
