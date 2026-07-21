#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
待办事项管理器 todo_manager.py
数据结构：列表存任务 dict；集合存标签去重
企业场景：个人任务看板，后续对接 Jira API
"""
# 启用未来注解语法，允许前向引用类型
from __future__ import annotations

# 从 dataclasses 导入装饰器与 field 工厂
from dataclasses import dataclass, field

# 导入 datetime 用于记录任务创建时间戳
from datetime import datetime

# 导入 Optional 表示可选类型（可为 None）
from typing import Optional


@dataclass
class TodoItem:
    """单条待办：使用 dataclass 减少样板 __init__ 代码。"""

    # 任务标题，必填字符串
    title: str
    # 是否已完成，默认 False 表示待办
    done: bool = False
    # 标签集合，set 保证不重复；default_factory 避免可变默认参数陷阱
    tags: set[str] = field(default_factory=set)
    # 创建时间 ISO 格式字符串，自动生成
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )
    # 优先级 1(高) 到 5(低)，默认 3 为普通
    priority: int = 3

    def toggle(self) -> None:
        """切换完成状态：True变False，False变True。"""
        # 取反布尔字段
        self.done = not self.done

    def add_tag(self, tag: str) -> None:
        """向当前任务添加单个标签。"""
        # strip 去除首尾空白
        cleaned = tag.strip()
        # 非空才加入集合
        if cleaned:
            self.tags.add(cleaned)


class TodoManager:
    """内存版待办管理器，支持增删改查、标签过滤与排序。"""

    def __init__(self) -> None:
        # 私有列表存储 TodoItem 实例，下标即展示 ID
        self._items: list[TodoItem] = []

    def add(self, title: str, tags: Optional[set[str]] = None, priority: int = 3) -> TodoItem:
        """添加新任务，返回创建的 TodoItem 对象。"""
        # 规范化标题
        title = title.strip()
        # 业务校验：标题不能为空
        if not title:
            raise ValueError("标题不能为空")
        # 优先级限制在 1-5
        priority = max(1, min(5, priority))
        # 构造实体
        item = TodoItem(title=title, tags=tags or set(), priority=priority)
        # 追加到内部列表尾部
        self._items.append(item)
        return item

    def list_all(self) -> list[TodoItem]:
        """返回全部任务的浅拷贝列表，防止外部直接改内部状态。"""
        return list(self._items)

    def list_by_tag(self, tag: str) -> list[TodoItem]:
        """过滤包含指定标签的任务。"""
        tag = tag.strip()
        return [i for i in self._items if tag in i.tags]

    def list_pending(self) -> list[TodoItem]:
        """仅返回未完成任务。"""
        return [i for i in self._items if not i.done]

    def mark_done(self, index: int) -> None:
        """按索引标记为已完成。"""
        # 边界检查
        if index < 0 or index >= len(self._items):
            raise IndexError("索引越界")
        # 设置 done 标志
        self._items[index].done = True

    def toggle_at(self, index: int) -> None:
        """按索引切换完成状态。"""
        if index < 0 or index >= len(self._items):
            raise IndexError("索引越界")
        self._items[index].toggle()

    def remove(self, index: int) -> TodoItem:
        """删除并返回被移除的任务。"""
        if index < 0 or index >= len(self._items):
            raise IndexError("索引越界")
        return self._items.pop(index)

    def sort_by_priority(self) -> None:
        """按 priority 升序原地排序（数字越小越靠前）。"""
        self._items.sort(key=lambda x: x.priority)

    def unique_tags(self) -> set[str]:
        """汇总所有任务中出现过的标签（去重）。"""
        result: set[str] = set()
        for item in self._items:
            # 集合并集更新
            result |= item.tags
        return result

    def stats(self) -> dict[str, int]:
        """统计总任务数、已完成、待办数量。"""
        total = len(self._items)
        done = sum(1 for i in self._items if i.done)
        return {"total": total, "done": done, "pending": total - done}

    def render(self) -> str:
        """渲染 ASCII 表格字符串，便于终端打印。"""
        lines = ["ID | 状态 | 优先级 | 标题 | 标签", "-" * 58]
        for idx, item in enumerate(self._items):
            status = "✓" if item.done else " "
            tags = ",".join(sorted(item.tags)) or "-"
            lines.append(
                f"{idx:2d} | [{status}] | P{item.priority} | {item.title} | {tags}"
            )
        return "\n".join(lines)


def demo() -> None:
    """演示：创建管理器、添加样例、排序并打印。"""
    mgr = TodoManager()
    mgr.add("完成 env_check 文档", {"devops", "day1"}, priority=2)
    mgr.add("实现 text_cleaner 单测", {"python", "day2"}, priority=1)
    mgr.add("复习流程控制", {"python", "day3"}, priority=3)
    mgr.mark_done(0)
    mgr.sort_by_priority()
    print(mgr.render())
    print("统计:", mgr.stats())
    print("全部标签:", mgr.unique_tags())
    print("标签 python:", [i.title for i in mgr.list_by_tag("python")])
    print("待办:", [i.title for i in mgr.list_pending()])


def main() -> None:
    demo()


if __name__ == "__main__":
    main()
