"""nexus_cli 自定义异常层次。

企业代码应使用语义化异常，便于上层统一捕获与日志分类。
"""
from __future__ import annotations


class NexusCLIError(Exception):
    """所有 Nexus CLI 异常的基类。"""

    def __init__(self, message: str, code: str = "NEXUS_CLI_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ValidationError(NexusCLIError):
    """输入校验失败。"""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="VALIDATION_ERROR")


class CommandNotFoundError(NexusCLIError):
    """未知子命令。"""

    def __init__(self, command: str) -> None:
        super().__init__(f"未知命令: {command}", code="COMMAND_NOT_FOUND")
        self.command = command
