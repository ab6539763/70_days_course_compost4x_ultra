#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运算符演示 operators_demo.py — Day 2 上午理论配套
覆盖：算术、比较、逻辑运算符及优先级
企业场景：计算 API Token 费用估算、批量任务分页
"""

# 算术运算符：+ - * / // % **
# 在 NexusAgent 中用于：token 计数、分页 offset、批处理 chunk 计算

# 定义一批待处理的文档数量（模拟 RAG 入库任务）
total_documents = 127

# 每批处理条数（整除 // 用于计算完整批次数）
batch_size = 10

# 使用整除计算完整批次数（向下取整）
full_batches = total_documents // batch_size

# 使用取模计算最后一批剩余条数
remainder = total_documents % batch_size

# 浮点除法计算平均每批耗时（秒），用于 SLA 估算
avg_seconds_per_doc = 0.35
estimated_batch_seconds = batch_size * avg_seconds_per_doc

# 幂运算：** 用于指数退避重试间隔（2^n 秒）
retry_attempt = 3
backoff_seconds = 2 ** retry_attempt  # 2^3 = 8 秒

# 比较运算符：== != < > <= >=
# 用于判断 API 响应状态、阈值告警

# 模拟 API 返回的 HTTP 状态码
http_status = 200

# 判断请求是否成功（2xx）
is_success = http_status >= 200 and http_status < 300

# 判断是否需要重试（5xx 服务端错误）
needs_retry = http_status >= 500

# 字符串长度与 token 上限比较（后续 Day15 会深入）
prompt_chars = 3200
max_chars = 4000
within_limit = prompt_chars <= max_chars

# 逻辑运算符：and or not
# 用于组合多个业务条件

# 是否允许写入知识库：成功 且 未超长 且 非空
content_nonempty = True
can_ingest = is_success and within_limit and content_nonempty

# 是否触发降级：失败 或 超长
use_fallback = not is_success or not within_limit

# 运算符优先级演示：先乘除后加减
# 错误写法：total = 100 + 50 * 2  → 先算 50*2=100，再加 100 = 200
price_per_1k_tokens = 0.002
token_count = 1500
# 正确：先除法再乘法（千 token 计费）
cost_yuan = (token_count / 1000) * price_per_1k_tokens

# 使用括号明确优先级，企业代码推荐显式括号
cost_yuan_explicit = (token_count / 1000.0) * price_per_1k_tokens


def format_report() -> str:
    """用 f-string 生成可读报告（连接下午 prompt_fstring.py 主题）"""
    lines = [
        "=" * 52,
        "  智链科技 · 运算符演示报告（Day 2）",
        "=" * 52,
        f"文档总数: {total_documents} | 批大小: {batch_size}",
        f"完整批次: {full_batches} | 余数: {remainder}",
        f"预估单批耗时: {estimated_batch_seconds:.2f} 秒",
        f"重试退避(第{retry_attempt}次): {backoff_seconds} 秒",
        "-" * 52,
        f"HTTP {http_status} | 成功={is_success} | 需重试={needs_retry}",
        f"Prompt {prompt_chars} 字符 | 上限 {max_chars} | 合规={within_limit}",
        f"可入库={can_ingest} | 降级={use_fallback}",
        f"Token 费用估算: ¥{cost_yuan_explicit:.6f}",
        "=" * 52,
    ]
    return "\n".join(lines)


def main() -> None:
    """程序入口"""
    print(format_report())
    print("\n✅ 运算符演示完成。请修改顶部变量观察输出变化。")


if __name__ == "__main__":
    main()
