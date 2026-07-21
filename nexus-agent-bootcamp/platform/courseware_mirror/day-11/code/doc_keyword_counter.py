#!/usr/bin/env python3
"""
Day 11 示例：文档关键词统计器 —— 文件 IO + 正则表达式

场景：企业知识库上传前，自动扫描文档中的敏感词、高频技术术语，
      为 RAG 索引质量评估提供基础数据（Day 25+ 会扩展为完整管道）。
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


# 默认关注的技术关键词（可扩展为从配置文件加载）
DEFAULT_KEYWORDS: list[str] = [
    "Python", "API", "Agent", "RAG", "向量", "嵌入",
    "大模型", "LLM", "微调", "Docker", "FastAPI",
]

# 编译正则：整词匹配，忽略大小写（中文无边界，直接子串匹配）
def build_pattern(keywords: list[str]) -> re.Pattern[str]:
    """将关键词列表编译为单一正则表达式。"""
    escaped = [re.escape(kw) for kw in keywords]
    # 英文用词边界 \b，中文直接匹配
    parts = []
    for kw, esc in zip(keywords, escaped):
        if re.match(r"^[A-Za-z0-9]+$", kw):
            parts.append(rf"\b{esc}\b")
        else:
            parts.append(esc)
    return re.compile("|".join(parts), re.IGNORECASE)


def read_text_file(path: Path, encoding: str = "utf-8") -> str:
    """
    安全读取文本文件，自动处理常见编码问题。

    Raises:
        FileNotFoundError: 文件不存在
        UnicodeDecodeError: 编码无法解码（会尝试 gbk 回退）
    """
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"路径是目录而非文件: {path}")

    try:
        return path.read_text(encoding=encoding)
    except UnicodeDecodeError:
        # Windows 用户可能用 GBK 保存的文档
        return path.read_text(encoding="gbk", errors="replace")


def count_keywords(text: str, pattern: re.Pattern[str]) -> Counter[str]:
    """统计文本中各关键词出现次数。"""
    counter: Counter[str] = Counter()
    for match in pattern.finditer(text):
        counter[match.group().lower() if match.group().isascii() else match.group()] += 1
    return counter


def scan_file(path: Path, keywords: list[str] | None = None) -> dict:
    """
    扫描单个文件，返回统计报告字典。

    Returns:
        {
            "file": str,
            "total_chars": int,
            "total_lines": int,
            "keyword_hits": dict[str, int],
            "top_keywords": list[tuple[str, int]],
        }
    """
    keywords = keywords or DEFAULT_KEYWORDS
    pattern = build_pattern(keywords)
    text = read_text_file(path)

    lines = text.splitlines()
    hits = count_keywords(text, pattern)

    return {
        "file": str(path),
        "total_chars": len(text),
        "total_lines": len(lines),
        "keyword_hits": dict(hits),
        "top_keywords": hits.most_common(5),
    }


def scan_directory(dir_path: Path, glob_pattern: str = "*.md") -> list[dict]:
    """批量扫描目录下匹配的文档。"""
    reports = []
    for fp in sorted(dir_path.glob(glob_pattern)):
        if fp.is_file():
            reports.append(scan_file(fp))
    return reports


def print_report(report: dict) -> None:
    """格式化打印单文件报告。"""
    print(f"\n{'='*50}")
    print(f"文件: {report['file']}")
    print(f"字符数: {report['total_chars']}  |  行数: {report['total_lines']}")
    print("关键词命中:")
    if report["top_keywords"]:
        for kw, cnt in report["top_keywords"]:
            print(f"  - {kw}: {cnt}")
    else:
        print("  (无匹配)")


def main() -> None:
    """命令行入口：python doc_keyword_counter.py <文件或目录>"""
    if len(sys.argv) < 2:
        # 无参数时扫描内置示例文档
        sample = Path(__file__).parent / "sample_docs" / "intro.md"
        sample.parent.mkdir(parents=True, exist_ok=True)
        if not sample.exists():
            sample.write_text(
                """# NexusAgent 简介

NexusAgent 是智链科技的企业级 Agent 平台，基于 Python 与 FastAPI 构建。
支持 RAG 检索增强、多 Agent 协作与大模型 API 接入。

## 技术栈
- Python 3.10+
- 向量数据库
- LLM API（通义千问、DeepSeek）
""",
                encoding="utf-8",
            )
        target = sample
    else:
        target = Path(sys.argv[1])

    if target.is_dir():
        reports = scan_directory(target)
    else:
        reports = [scan_file(target)]

    for r in reports:
        print_report(r)

    total_hits = sum(sum(r["keyword_hits"].values()) for r in reports)
    print(f"\n{'='*50}")
    print(f"共扫描 {len(reports)} 个文件，关键词总命中 {total_hits} 次")


if __name__ == "__main__":
    main()
