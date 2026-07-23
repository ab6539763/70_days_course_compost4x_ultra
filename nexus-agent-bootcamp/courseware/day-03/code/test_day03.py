#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Day 3 全链路单元测试 — 运行: python3 -m pytest test_day03.py -v"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))

from flow_control_basics import (  # noqa: E402
    batch_indices,
    label_lines,
    score_to_grade,
    simulate_retry,
)
from guess_number import compare_guess, is_valid_guess_input, play_round  # noqa: E402
from multiplication_table import build_row, build_table  # noqa: E402
from menu_system import build_actions, run_menu  # noqa: E402


class TestFlowControlBasics:
    def test_simulate_retry_breaks_at_3(self) -> None:
        waits = simulate_retry()
        assert len(waits) == 3
        assert waits == [2, 4, 8]

    def test_batch_indices(self) -> None:
        batches = batch_indices(25, 10)
        assert batches == [(0, 10), (10, 20), (20, 25)]

    def test_label_lines(self) -> None:
        assert label_lines(["a", "b"]) == ["001| a", "002| b"]

    def test_score_to_grade(self) -> None:
        assert score_to_grade(95) == "A"
        assert score_to_grade(55) == "D"


class TestGuessNumber:
    def test_compare_guess(self) -> None:
        assert compare_guess(10, 20) == "low"
        assert compare_guess(30, 20) == "high"
        assert compare_guess(20, 20) == "win"

    def test_is_valid_guess_input(self) -> None:
        assert is_valid_guess_input("50") is True
        assert is_valid_guess_input("abc") is False
        assert is_valid_guess_input("0") is False
        assert is_valid_guess_input("101") is False

    def test_play_round_win(self) -> None:
        inputs = iter(["50", "42"])
        won = play_round(target=42, input_fn=lambda _: next(inputs), print_fn=lambda _: None)
        assert won is True

    def test_play_round_lose(self) -> None:
        inputs = iter(["1"] * 10)
        won = play_round(target=99, input_fn=lambda _: next(inputs), print_fn=lambda _: None, max_attempts=3)
        assert won is False


class TestMultiplicationTable:
    def test_build_row(self) -> None:
        row = build_row(3)
        assert "1×3= 3" in row
        assert "3×3= 9" in row

    def test_build_table_size(self) -> None:
        assert len(build_table(5)) == 5

    def test_invalid_size(self) -> None:
        with pytest.raises(ValueError):
            build_table(10)


class TestMenuSystem:
    def test_build_actions_keys(self) -> None:
        actions = build_actions(print_fn=lambda _: None)
        assert set(actions.keys()) == {"1", "2", "3"}

    def test_run_menu_scripted(self) -> None:
        logs: list[str] = []
        inputs = iter(["1", "0"])
        run_menu(input_fn=lambda _: next(inputs), print_fn=logs.append)
        assert any("v0.1-day03" in line for line in logs)
        assert any("再见" in line for line in logs)


class TestScriptsRunnable:
    @pytest.mark.parametrize(
        "cmd",
        [
            ["flow_control_basics.py"],
            ["guess_number.py", "--demo"],
            ["multiplication_table.py", "--size", "5"],
            ["menu_system.py", "--test"],
        ],
    )
    def test_script_runs(self, cmd: list[str]) -> None:
        r = subprocess.run(
            [sys.executable, str(CODE_DIR / cmd[0]), *cmd[1:]],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(CODE_DIR),
        )
        assert r.returncode == 0, f"{cmd} failed:\n{r.stderr}\n{r.stdout}"
        assert "✅" in r.stdout


class TestHomework:
    def test_homework_self_test(self) -> None:
        hw = CODE_DIR.parent / "homework" / "menu_extended.py"
        r = subprocess.run(
            [sys.executable, str(hw), "--test"],
            capture_output=True,
            text=True,
            timeout=20,
            cwd=str(hw.parent),
        )
        assert r.returncode == 0, r.stderr
        assert "作业自测通过" in r.stdout
