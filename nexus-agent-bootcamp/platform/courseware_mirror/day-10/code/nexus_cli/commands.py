"""nexus_cli 子命令实现模块。"""
from __future__ import annotations

import argparse

from nexus_cli import __version__
from nexus_cli.exceptions import CommandNotFoundError
from nexus_cli.utils import banner, validate_name


def run_greet(name: str) -> None:
    """greet 子命令：向指定用户问好。"""
    validate_name(name)
    print(banner())
    print(f"你好，{name}！欢迎使用 Nexus CLI v{__version__}")


def run_version() -> None:
    """version 子命令：打印版本号。"""
    print(f"nexus_cli/{__version__}")


def build_parser() -> argparse.ArgumentParser:
    """构建 argparse 解析器，定义子命令。"""
    parser = argparse.ArgumentParser(prog="nexus_cli", description="Nexus 命令行工具")
    sub = parser.add_subparsers(dest="command", required=True)

    greet_p = sub.add_parser("greet", help="问候用户")
    greet_p.add_argument("name", help="用户名")

    sub.add_parser("version", help="显示版本")

    return parser


def dispatch(argv: list[str]) -> int:
    """根据 argv 分发到对应子命令处理函数。"""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "greet":
        run_greet(args.name)
    elif args.command == "version":
        run_version()
    else:
        raise CommandNotFoundError(args.command)
    return 0
