#!/usr/bin/env bash
# Day 2 全链路验证脚本 — 讲师/学员自检用
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DAY02="$ROOT/courseware/day-02"
CODE="$DAY02/code"

echo "=========================================="
echo " Day 02 全链路验证"
echo "=========================================="

# 1. Python 版本
python3 --version | grep -E "3\.(1[0-9]|[2-9][0-9])" || {
  echo "❌ 需要 Python 3.10+"
  exit 1
}
echo "✅ Python 版本检查通过"

# 2. 编译检查
python3 -m compileall -q "$CODE"
echo "✅ 语法编译检查通过"

# 3. 逐个运行主脚本
for script in operators_demo.py string_basics.py prompt_fstring.py text_cleaner.py; do
  echo "--- 运行 $script ---"
  python3 "$CODE/$script" | tail -3
done
echo "✅ 全部主脚本运行通过"

# 4. 文件批处理模式
python3 "$CODE/text_cleaner.py" --file "$DAY02/assets/sample_comments.txt" | tail -5
echo "✅ 文件批处理模式通过"

# 5. 作业答案
python3 "$DAY02/homework/text_cleaner_hw.py"
echo "✅ 作业自测通过"

# 6. pytest（若已安装）
if python3 -c "import pytest" 2>/dev/null; then
  python3 -m pytest "$CODE/test_day02.py" -q --tb=short
  echo "✅ pytest 单元测试通过"
else
  pip install pytest -q
  python3 -m pytest "$CODE/test_day02.py" -q --tb=short
  echo "✅ pytest 单元测试通过（已自动安装 pytest）"
fi

# 7. 课件字数
CHARS=$(wc -c < "$DAY02/README.md")
if [ "$CHARS" -lt 20000 ]; then
  echo "⚠️  README 字数 ${CHARS} < 20000，请补充课件"
  exit 1
fi
echo "✅ README 字数: ${CHARS} (≥20000)"

# 8. verify_day 工具
python3 "$ROOT/scripts/verify_day.py" --day 2
echo "✅ verify_day 通过"

echo "=========================================="
echo " 🎉 Day 02 全链路验证 100% 通过"
echo "=========================================="
