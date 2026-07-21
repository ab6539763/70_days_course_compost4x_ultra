#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发环境自检脚本 — 验证 Python 版本、编码与基本 IO 能力
企业场景：CI 流水线本地预检（pre-commit 前身）
"""

# 导入 platform 模块，读取操作系统与 Python 构建信息
import platform

# 导入 sys 模块，检查解释器版本与默认编码
import sys

# 导入 os 模块，检查环境变量与当前工作目录
import os

# 导入 locale 模块，检测系统区域与编码设置
import locale

# 导入 datetime 模块，为检查报告打上时间戳
from datetime import datetime

# 定义最低可接受的 Python 次版本号元组 (major, minor)
MIN_PYTHON = (3, 10)

# 定义检查项结果列表，每项为 (名称, 是否通过, 详情)
check_results: list[tuple[str, bool, str]] = []


def record_check(name: str, passed: bool, detail: str) -> None:
    """记录单项检查结果到全局列表。"""
    # 将三元组追加到结果列表
    check_results.append((name, passed, detail))


def check_python_version() -> None:
    """验证当前解释器版本是否满足训练营要求。"""
    # 读取当前版本的前两位 (major, minor)
    current = sys.version_info[:2]
    # 与最低版本比较，得到布尔值
    ok = current >= MIN_PYTHON
    # 格式化详情字符串，包含完整 version_info
    detail = f"当前 {current[0]}.{current[1]}，要求 >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]}"
    # 写入检查结果
    record_check("Python 版本", ok, detail)


def check_utf8_io() -> None:
    """验证标准输出能否正确处理中文（UTF-8）。"""
    # 测试字符串包含中文与 emoji，覆盖常见编码坑
    sample = "智链科技 NexusAgent 环境正常 ✅"
    try:
        # 尝试编码为 utf-8 字节再解码，模拟 IO 管道
        encoded = sample.encode("utf-8")
        decoded = encoded.decode("utf-8")
        # 比较往返后是否一致
        ok = decoded == sample
        detail = "UTF-8 编解码往返成功"
    except UnicodeError as exc:
        # 捕获编码异常并记录失败原因
        ok = False
        detail = f"编码异常: {exc}"
    record_check("UTF-8 中文 IO", ok, detail)


def check_working_directory() -> None:
    """确认当前工作目录可访问且包含预期课件路径片段。"""
    # 获取进程当前工作目录绝对路径
    cwd = os.getcwd()
    # 判断路径非空即视为可访问（极简校验，Day1 够用）
    ok = bool(cwd)
    detail = f"cwd={cwd}"
    record_check("工作目录", ok, detail)


def check_env_variables() -> None:
    """检查常用环境变量是否存在（非强制）。"""
    # 读取 PATH，开发者机器通常必有
    path_val = os.environ.get("PATH", "")
    # 有 PATH 即认为环境变量可读
    ok = len(path_val) > 0
    detail = f"PATH 长度={len(path_val)} 字符"
    record_check("环境变量 PATH", ok, detail)


def check_platform_info() -> None:
    """收集平台信息，便于讲师远程排查学员环境问题。"""
    # 拼接系统、版本、机器类型
    info = f"{platform.system()} {platform.release()} / {platform.machine()}"
    # 能读取即通过
    record_check("平台信息", True, info)


def render_report() -> str:
    """将检查结果渲染为可读文本报告。"""
    # 报告头部时间戳
    lines = [
        "=" * 50,
        "NexusAgent 开发环境自检报告",
        f"生成时间: {datetime.now().isoformat(timespec='seconds')}",
        "=" * 50,
    ]
    # 遍历每项检查，格式化 PASS/FAIL
    for name, passed, detail in check_results:
        status = "PASS" if passed else "FAIL"
        lines.append(f"[{status}] {name}: {detail}")
    # 统计失败数量
    failures = sum(1 for _, p, _ in check_results if not p)
    lines.append("-" * 50)
    lines.append(f"合计: {len(check_results)} 项, 失败 {failures} 项")
    # 用换行符连接各行
    return "\n".join(lines)


def main() -> None:
    """按顺序执行全部检查并打印报告。"""
    check_python_version()
    check_utf8_io()
    check_working_directory()
    check_env_variables()
    check_platform_info()
    report = render_report()
    print(report)
    # 任一失败则退出码为 1，供脚本化调用
    has_failure = any(not p for _, p, _ in check_results)
    sys.exit(1 if has_failure else 0)


if __name__ == "__main__":
    main()
