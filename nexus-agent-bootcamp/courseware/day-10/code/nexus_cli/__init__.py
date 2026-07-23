"""
nexus_cli — 智链科技 Nexus 命令行工具包（Day 10 教学示例）

包结构说明:
    nexus_cli/
    ├── __init__.py      # 包入口，导出公共 API
    ├── __main__.py      # python -m nexus_cli 入口
    ├── commands.py      # 子命令实现
    ├── utils.py         # 工具函数
    └── exceptions.py    # 自定义异常层次
"""
from nexus_cli.commands import run_greet, run_version
from nexus_cli.exceptions import NexusCLIError

__version__ = "0.1.0"
__all__ = ["run_greet", "run_version", "NexusCLIError", "__version__"]
