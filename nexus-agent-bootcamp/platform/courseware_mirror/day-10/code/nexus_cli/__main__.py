#!/usr/bin/env python3
"""
包模块入口：python -m nexus_cli

Python 通过 __main__.py 支持将包作为脚本运行。
"""
from __future__ import annotations

import sys

from nexus_cli.commands import dispatch
from nexus_cli.exceptions import NexusCLIError


def main(argv: list[str] | None = None) -> int:
    """CLI 主函数，返回进程退出码（0=成功，非0=失败）。"""
    argv = argv if argv is not None else sys.argv[1:]
    try:
        return dispatch(argv)
    except NexusCLIError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n已取消", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
