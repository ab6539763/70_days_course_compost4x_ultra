#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通讯录管理器 contact_manager.py — Week1 综合项目
功能：完整 CRUD + JSON 文件持久化 + 命令行菜单
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional


DEFAULT_DB = Path("data/contacts.json")


@dataclass
class Contact:
    """联系人实体。"""
    name: str
    phone: str
    email: str = ""
    company: str = "智链科技"
    tags: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name.strip():
            errors.append("姓名不能为空")
        if not self.phone.strip():
            errors.append("电话不能为空")
        if self.email and "@" not in self.email:
            errors.append("邮箱格式不正确")
        return errors


class ContactRepository:
    """JSON 文件持久化仓储。"""

    def __init__(self, db_path: Path = DEFAULT_DB) -> None:
        self.db_path = db_path
        self._contacts: list[Contact] = []
        self.load()

    def load(self) -> None:
        if not self.db_path.exists():
            self._contacts = []
            return
        raw = json.loads(self.db_path.read_text(encoding="utf-8"))
        self._contacts = [Contact(**item) for item in raw]

    def save(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        data = [asdict(c) for c in self._contacts]
        self.db_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def all(self) -> list[Contact]:
        return list(self._contacts)

    def add(self, contact: Contact) -> None:
        errors = contact.validate()
        if errors:
            raise ValueError("; ".join(errors))
        self._contacts.append(contact)
        self.save()

    def get(self, index: int) -> Contact:
        return self._contacts[index]

    def update(self, index: int, **fields: Any) -> Contact:
        contact = self._contacts[index]
        for key, value in fields.items():
            if hasattr(contact, key):
                setattr(contact, key, value)
        errors = contact.validate()
        if errors:
            raise ValueError("; ".join(errors))
        self.save()
        return contact

    def delete(self, index: int) -> Contact:
        removed = self._contacts.pop(index)
        self.save()
        return removed

    def search(self, keyword: str) -> list[Contact]:
        key = keyword.lower()
        return [
            c
            for c in self._contacts
            if key in c.name.lower()
            or key in c.phone
            or key in c.email.lower()
            or any(key in t.lower() for t in c.tags)
        ]


class ContactCLI:
    """命令行界面。"""

    def __init__(self, repo: ContactRepository) -> None:
        self.repo = repo

    def render_table(self) -> None:
        contacts = self.repo.all()
        if not contacts:
            print("(通讯录为空，请先添加)")
            return
        print(f"{'ID':>3} | {'姓名':<8} | {'电话':<13} | {'邮箱':<20} | 标签")
        print("-" * 65)
        for i, c in enumerate(contacts):
            tags = ",".join(c.tags) or "-"
            print(f"{i:3d} | {c.name:<8} | {c.phone:<13} | {c.email:<20} | {tags}")

    def action_list(self) -> None:
        self.render_table()

    def action_add(self) -> None:
        name = input("姓名: ").strip()
        phone = input("电话: ").strip()
        email = input("邮箱(可空): ").strip()
        tags_raw = input("标签(逗号分隔,可空): ").strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        try:
            self.repo.add(Contact(name=name, phone=phone, email=email, tags=tags))
            print("添加成功")
        except ValueError as exc:
            print(f"添加失败: {exc}")

    def action_update(self) -> None:
        self.render_table()
        idx = self._read_index()
        if idx is None:
            return
        phone = input("新电话(回车跳过): ").strip()
        email = input("新邮箱(回车跳过): ").strip()
        fields: dict[str, Any] = {}
        if phone:
            fields["phone"] = phone
        if email:
            fields["email"] = email
        try:
            self.repo.update(idx, **fields)
            print("更新成功")
        except (IndexError, ValueError) as exc:
            print(f"更新失败: {exc}")

    def action_delete(self) -> None:
        self.render_table()
        idx = self._read_index()
        if idx is None:
            return
        try:
            removed = self.repo.delete(idx)
            print(f"已删除: {removed.name}")
        except IndexError:
            print("索引无效")

    def action_search(self) -> None:
        keyword = input("搜索关键词: ").strip()
        results = self.repo.search(keyword)
        if not results:
            print("无匹配结果")
            return
        for c in results:
            print(f"- {c.name} {c.phone} {c.email}")

    def _read_index(self) -> Optional[int]:
        raw = input("输入 ID: ").strip()
        if not raw.isdigit():
            print("无效 ID")
            return None
        return int(raw)

    def run(self) -> None:
        actions = {
            "1": ("列出全部", self.action_list),
            "2": ("添加联系人", self.action_add),
            "3": ("更新联系人", self.action_update),
            "4": ("删除联系人", self.action_delete),
            "5": ("搜索", self.action_search),
        }
        print("=" * 40)
        print("  NexusAgent 通讯录 Week1 收官项目")
        print("=" * 40)
        while True:
            for key, (label, _) in actions.items():
                print(f"  {key}. {label}")
            print("  0. 保存并退出")
            choice = input("请选择: ").strip()
            if choice == "0":
                self.repo.save()
                print("数据已保存，再见！")
                break
            entry = actions.get(choice)
            if entry is None:
                print("无效选项")
                continue
            entry[1]()
            print("-" * 40)


def seed_demo_data(repo: ContactRepository) -> None:
    if repo.all():
        return
    repo.add(Contact("张晓明", "13800001111", "zhang@smartlink.cn", tags=["研发"]))
    repo.add(Contact("林悦", "13900002222", "linyue@smartlink.cn", tags=["产品"]))
    repo.add(Contact("陈建国", "13700003333", "chen@smartlink.cn", tags=["研发", "lead"]))


def main() -> None:
    repo = ContactRepository()
    seed_demo_data(repo)
    cli = ContactCLI(repo)
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n中断退出，已尝试保存")
        repo.save()
        sys.exit(0)


if __name__ == "__main__":
    main()
