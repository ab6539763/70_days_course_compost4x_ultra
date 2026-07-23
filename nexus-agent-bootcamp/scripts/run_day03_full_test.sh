#!/usr/bin/env bash
# Day 3 全链路验证脚本
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DAY03="$ROOT/courseware/day-03"
CODE="$DAY03/code"

echo "=========================================="
echo " Day 03 全链路验证"
echo "=========================================="

python3 --version | grep -E "3\.(1[0-9]|[2-9][0-9])" || { echo "❌ 需要 Python 3.10+"; exit 1; }
echo "✅ Python 版本检查通过"

python3 -m compileall -q "$CODE"
echo "✅ 语法编译检查通过"

# 3. 逐个运行主脚本
python3 "$CODE/flow_control_basics.py" | tail -2
python3 "$CODE/guess_number.py" --demo | tail -2
python3 "$CODE/multiplication_table.py" | tail -2
python3 "$CODE/multiplication_table.py" --size 5 | tail -2
python3 "$CODE/menu_system.py" --test | tail -2
echo "✅ 全部主脚本运行通过"

python3 "$DAY03/homework/menu_extended.py" --test
echo "✅ 作业自测通过"

if python3 -c "import pytest" 2>/dev/null; then
  python3 -m pytest "$CODE/test_day03.py" -q --tb=short
else
  pip install pytest -q
  python3 -m pytest "$CODE/test_day03.py" -q --tb=short
fi
echo "✅ pytest 单元测试通过"

CHARS=$(wc -c < "$DAY03/README.md")
if [ "$CHARS" -lt 20000 ]; then
  echo "⚠️  README 字数 ${CHARS} < 20000"
  exit 1
fi
echo "✅ README 字数: ${CHARS} (≥20000)"

python3 "$ROOT/scripts/verify_day.py" --day 3
echo "✅ verify_day 通过"

echo "=========================================="
echo " 🎉 Day 03 全链路验证 100% 通过"
echo "=========================================="
