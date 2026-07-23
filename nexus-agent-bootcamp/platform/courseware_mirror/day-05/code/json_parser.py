#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON 解析与生成 json_parser.py
企业场景：读取 API 响应、配置文件、工单导出
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SAMPLE_TICKET = {
    "id": "NEXUS-1024",
    "title": "实现用户登录 API",
    "status": "In Progress",
    "assignee": {"name": "张晓明", "email": "zhang@smartlink.cn"},
    "labels": ["backend", "p0"],
    "story_points": 5,
}


def to_json_string(data: Any, *, pretty: bool = True) -> str:
    """Python 对象序列化为 JSON 字符串。"""
    indent = 2 if pretty else None
    return json.dumps(data, ensure_ascii=False, indent=indent)


def from_json_string(text: str) -> Any:
    """JSON 字符串反序列化为 Python 对象。"""
    return json.loads(text)


def load_json_file(path: Path) -> Any:
    """从 UTF-8 文件读取 JSON。"""
    content = path.read_text(encoding="utf-8")
    return json.loads(content)


def save_json_file(path: Path, data: Any) -> None:
    """将对象写入 JSON 文件，自动创建父目录。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text + "\n", encoding="utf-8")


def get_nested(data: dict[str, Any], keys: list[str], default: Any = None) -> Any:
    """安全读取嵌套字典，任一层缺失返回 default。"""
    current: Any = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def validate_ticket(ticket: dict[str, Any]) -> list[str]:
    """校验工单必填字段，返回错误列表（空即通过）。"""
    errors: list[str] = []
    required = ["id", "title", "status"]
    for field in required:
        if field not in ticket or not ticket[field]:
            errors.append(f"缺少或为空: {field}")
    if "assignee" in ticket:
        email = get_nested(ticket, ["assignee", "email"])
        if email and "@" not in str(email):
            errors.append("assignee.email 格式可疑")
    return errors


def tickets_summary(tickets: list[dict[str, Any]]) -> dict[str, int]:
    """按 status 聚合计数。"""
    summary: dict[str, int] = {}
    for t in tickets:
        status = str(t.get("status", "Unknown"))
        summary[status] = summary.get(status, 0) + 1
    return summary


def demo() -> None:
    print("=== JSON 序列化 ===")
    text = to_json_string(SAMPLE_TICKET)
    print(text)
    print("=== 反序列化 ===")
    obj = from_json_string(text)
    print(type(obj), obj["id"])
    print("=== 嵌套读取 ===")
    print(get_nested(obj, ["assignee", "email"]))
    print("=== 校验 ===")
    print(validate_ticket(obj))
    tmp = Path("data/sample_ticket.json")
    save_json_file(tmp, SAMPLE_TICKET)
    loaded = load_json_file(tmp)
    print("=== 文件往返 ===", loaded["title"])
    batch = [SAMPLE_TICKET, {**SAMPLE_TICKET, "id": "NEXUS-1025", "status": "Done"}]
    print("=== 汇总 ===", tickets_summary(batch))


def main() -> None:
    demo()


if __name__ == "__main__":
    main()
