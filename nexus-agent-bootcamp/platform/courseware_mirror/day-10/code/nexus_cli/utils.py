"""nexus_cli 工具函数。"""
from __future__ import annotations

from nexus_cli.exceptions import ValidationError


def banner() -> str:
    """返回 ASCII 品牌横幅。"""
    return """
╔══════════════════════════════════╗
║     NexusAgent CLI  v0.1         ║
║     智链科技 SmartLink Tech      ║
╚══════════════════════════════════╝
""".strip()


def validate_name(name: str) -> None:
    """校验用户名：非空、长度 2-20、仅字母数字下划线中文。"""
    if not name or not name.strip():
        raise ValidationError("用户名不能为空")
    if len(name) > 20:
        raise ValidationError("用户名不能超过 20 个字符")
