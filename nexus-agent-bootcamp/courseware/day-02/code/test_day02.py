#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Day 2 全链路单元测试 — 运行: python3 -m pytest test_day02.py -v"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))

from text_cleaner import (  # noqa: E402
    batch_clean,
    clean_text,
    extract_hashtags,
    is_palindrome,
    mask_email,
    mask_phone_numbers,
    normalize_unicode,
    process_file,
    word_count,
)

ASSETS = CODE_DIR.parent / "assets" / "sample_comments.txt"


class TestCleanText:
    def test_empty_input(self) -> None:
        assert clean_text("") == ""

    def test_unicode_nfkc(self) -> None:
        assert "ABC123" in normalize_unicode("ＡＢＣ１２３")

    def test_url_removal(self) -> None:
        out = clean_text("见 https://a.com 文档")
        assert "[URL]" in out
        assert "https://" not in out

    def test_phone_mask(self) -> None:
        out = clean_text("电话13812345678")
        assert "138****5678" in out

    def test_email_mask(self) -> None:
        out = clean_text("邮箱 a@b.com 测试")
        assert "a***@b.com" in out

    def test_mention_replace(self) -> None:
        out = clean_text("@alice 你好")
        assert "@USER" in out
        assert "@alice" not in out

    def test_keyword_only_mask_phone_false(self) -> None:
        out = clean_text("13812345678", mask_phone=False)
        assert "13812345678" in out


class TestHelpers:
    def test_extract_hashtags(self) -> None:
        assert extract_hashtags("#A #中文") == ["A", "中文"]

    def test_mask_email_standalone(self) -> None:
        assert "z***@" in mask_email("zhang@smartlink.cn")

    def test_word_count(self) -> None:
        stats = word_count("hello world")
        assert stats["words"] == 2
        assert stats["chars"] == 11

    def test_batch_clean(self) -> None:
        lines = ["  a  ", "  b  "]
        results = batch_clean(lines)
        assert results == ["a", "b"]

    def test_is_palindrome(self) -> None:
        assert is_palindrome("上海自来水来自海上") is True
        assert is_palindrome("abc") is False


class TestFileIO:
    def test_process_sample_file(self) -> None:
        assert ASSETS.exists(), f"缺少测试数据: {ASSETS}"
        results = process_file(ASSETS)
        assert len(results) >= 5
        # 至少一行应含 URL 占位
        assert any("[URL]" in r for r in results)


class TestScriptsRunnable:
    @pytest.mark.parametrize(
        "script",
        ["operators_demo.py", "string_basics.py", "prompt_fstring.py", "text_cleaner.py"],
    )
    def test_script_runs(self, script: str) -> None:
        r = subprocess.run(
            [sys.executable, str(CODE_DIR / script)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(CODE_DIR),
        )
        assert r.returncode == 0, f"{script} failed:\n{r.stderr}"
        assert "✅" in r.stdout or "演示" in r.stdout or "样本" in r.stdout

    def test_text_cleaner_file_mode(self) -> None:
        r = subprocess.run(
            [sys.executable, "text_cleaner.py", "--file", str(ASSETS)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(CODE_DIR),
        )
        assert r.returncode == 0
        assert "已清洗" in r.stdout
