#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流程控制基础 flow_control_basics.py — Day 3 上午理论配套
覆盖：if/elif/else、while、for、range、break、continue
企业场景：API 重试循环、批处理遍历、状态机分支
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. if / elif / else — 分支判断
# ---------------------------------------------------------------------------
# 模拟 API 返回的 HTTP 状态码（Day 12 将真实调用）
http_status = 429  # Too Many Requests

# 单分支 if：仅成功时执行
if http_status == 200:
    message = "请求成功"
# 多分支 elif：按状态码分类处理策略
elif http_status == 401:
    message = "未授权，检查 API Key"
elif http_status == 429:
    message = "触发限流，等待后重试"
elif http_status >= 500:
    message = "服务端错误，指数退避重试"
else:
  # else：以上都不匹配时的兜底
    message = f"未知状态码 {http_status}"

# ---------------------------------------------------------------------------
# 2. 逻辑组合与嵌套 if
# ---------------------------------------------------------------------------
has_api_key = True
is_rate_limited = http_status == 429

# and：两个条件都满足才重试
should_retry = has_api_key and is_rate_limited

# ---------------------------------------------------------------------------
# 3. while 循环 — break / continue
# ---------------------------------------------------------------------------

def simulate_retry(max_retries: int = 5) -> list[int]:
    """
    模拟 API 重试：第 3 次成功则 break 跳出循环。
    返回每次尝试的等待秒数列表。
    """
    attempt = 0
    waits: list[int] = []
    while attempt < max_retries:
        attempt += 1
        wait_sec = 2 ** attempt  # 指数退避：2, 4, 8, 16, 32
        waits.append(wait_sec)
        if attempt == 3:
            # break：立即退出 while，不再继续
            break
        # continue 示例：若 wait_sec > 10 则跳过记录（此处仅演示语义）
        if wait_sec > 100:
            continue
    return waits


# ---------------------------------------------------------------------------
# 4. for 循环与 range()
# ---------------------------------------------------------------------------

def batch_indices(total: int, batch_size: int) -> list[tuple[int, int]]:
    """
    用 range(start, stop, step) 生成批处理起止下标。
    NexusAgent 文档入库批处理将复用此模式（Day 28）。
    """
    batches: list[tuple[int, int]] = []
    # range(0, total, batch_size) → 0, 10, 20, ...
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batches.append((start, end))
    return batches


# ---------------------------------------------------------------------------
# 5. enumerate — 遍历时需要索引
# ---------------------------------------------------------------------------

def label_lines(lines: list[str]) -> list[str]:
    """为每行加序号，模拟日志行号输出"""
    numbered: list[str] = []
    # enumerate 返回 (索引, 元素)，start=1 从 1 开始编号
    for idx, line in enumerate(lines, start=1):
        numbered.append(f"{idx:03d}| {line}")
    return numbered


# ---------------------------------------------------------------------------
# 6. 综合：根据分数输出等级（if-elif 链）
# ---------------------------------------------------------------------------

def score_to_grade(score: int) -> str:
    """周测分数转等级 — Day 7 周测将用到类似逻辑"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "D"


def format_report() -> str:
    """汇总今日流程控制演示结果"""
    lines = [
        "=" * 56,
        "  智链科技 · 流程控制基础演示（Day 3）",
        "=" * 56,
        f"HTTP {http_status} → {message}",
        f"应重试: {should_retry}",
        f"重试等待序列: {simulate_retry()}",
        f"批处理下标(127条/批10): {batch_indices(127, 10)[:3]}...",
        f"行号标注: {label_lines(['alpha', 'beta'])}",
        f"分数 85 → 等级 {score_to_grade(85)}",
        "=" * 56,
    ]
    return "\n".join(lines)


def main() -> None:
    print(format_report())
    print("\n✅ flow_control_basics 运行成功")


if __name__ == "__main__":
    main()
