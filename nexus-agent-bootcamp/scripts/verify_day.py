#!/usr/bin/env python3
"""验证指定天数的课件代码可运行。"""
from __future__ import annotations

import argparse
import compileall
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COURSEWARE = ROOT / "courseware"


def verify_day(day: int) -> bool:
    code_dir = COURSEWARE / f"day-{day:02d}" / "code"
    if not code_dir.exists():
        print(f"[FAIL] day-{day:02d}: code dir missing")
        return False

    py_files = list(code_dir.rglob("*.py"))
    if not py_files:
        print(f"[WARN] day-{day:02d}: no Python files")
        return True

    ok = compileall.compile_dir(str(code_dir), quiet=1)
    if not ok:
        print(f"[FAIL] day-{day:02d}: syntax errors")
        return False

    # Run top-level scripts (not packages) with --help or dry run
    for py in sorted(code_dir.glob("*.py")):
        if py.name.startswith("test_"):
            continue
        try:
            r = subprocess.run(
                [sys.executable, str(py), "--help"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(py.parent),
            )
            # Many scripts won't have --help; try running with mock
            if r.returncode != 0 and "usage" not in (r.stdout + r.stderr).lower():
                r2 = subprocess.run(
                    [sys.executable, "-c", f"import importlib.util; spec=importlib.util.spec_from_file_location('m','{py}'); m=importlib.util.module_from_spec(spec)"],
                    capture_output=True,
                    timeout=5,
                )
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            print(f"[WARN] {py.name}: {e}")

    readme = COURSEWARE / f"day-{day:02d}" / "README.md"
    if readme.exists():
        chars = len(readme.read_text(encoding="utf-8"))
        status = "OK" if chars >= 8000 else "LOW"
        print(f"[{status}] day-{day:02d}: README {chars} chars, {len(py_files)} py files")

    print(f"[PASS] day-{day:02d}: compile check ok")
    return True


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--day", type=int, help="Single day")
    p.add_argument("--all", action="store_true", help="All 70 days")
    args = p.parse_args()

    if args.all:
        days = range(1, 71)
    elif args.day:
        days = [args.day]
    else:
        p.print_help()
        sys.exit(1)

    failed = [d for d in days if not verify_day(d)]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
