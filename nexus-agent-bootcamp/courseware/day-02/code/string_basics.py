#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字符串基础 string_basics.py — Day 2 上午配套
覆盖：索引、切片、strip/split/join/replace/format、不可变性
"""

# 模拟从客服系统导出的原始评论（含多余空白与换行）
raw_comment = "  NexusAgent   很好用！\n请加快迭代速度。  "

# strip：去除首尾空白，返回【新字符串】，原串不变
stripped = raw_comment.strip()
# 验证不可变性：raw_comment 仍含首尾空格
assert raw_comment != stripped, "strip 应返回新对象"

# lstrip / rstrip 单侧剥离
left_only = raw_comment.lstrip()

# split：按空白切分为词列表（默认任意连续空白）
words = stripped.split()
word_count = len(words)

# join：用指定分隔符拼接列表为字符串（与 split 互为逆操作）
joined_with_pipe = "|".join(words)

# replace：子串替换（非正则，全部替换）
replaced = stripped.replace("NexusAgent", "灵犀平台")

# in 成员检测
has_keyword = "迭代" in stripped

# 索引：正向从 0 开始，负向从 -1 为最后一个字符
first_char = stripped[0]
last_char = stripped[-1]

# 切片 [start:end:step] — end 不包含，step 为步长
# 取前 10 个字符
head = stripped[:10]
# 跳过前 2 个字符
tail_from_2 = stripped[2:]
# 反转字符串（面试常考）
reversed_text = stripped[::-1]

# 切片用于手机号打码预览（完整实现在 text_cleaner.py）
phone = "13812345678"
masked_preview = phone[:3] + "****" + phone[-4:]

# 旧式 format 与 f-string 对比
legacy = "用户 {} 提交了 {} 条反馈".format("张三", word_count)
modern = f"用户 张三 提交了 {word_count} 条反馈"
assert legacy == modern

# upper / lower / title 大小写
normalized_title = "smartlink nexus".title()


def demonstrate_immutability() -> None:
    """演示字符串不可变性 — 企业里关系到 dict key 与缓存"""
    s1 = "hello"
    s2 = s1
    # id 相同，指向同一对象
    same_object = id(s1) == id(s2)
    # upper 创建新对象
    s3 = s1.upper()
    different_object = id(s1) != id(s3)
    print(f"  s1 is s2: {same_object}")
    print(f"  s1.upper() 是新对象: {different_object}")


def main() -> None:
    print("=" * 56)
    print("  字符串基础演示 — Day 2")
    print("=" * 56)
    print(f"原始 repr : {raw_comment!r}")
    print(f"strip 后  : {stripped!r}")
    print(f"split 词数: {word_count} → {words}")
    print(f"join 管道 : {joined_with_pipe}")
    print(f"replace   : {replaced}")
    print(f"含「迭代」: {has_keyword}")
    print(f"首/末字符 : {first_char!r} / {last_char!r}")
    print(f"切片 head : {head!r}")
    print(f"反转      : {reversed_text!r}")
    print(f"手机打码  : {masked_preview}")
    print(f"format    : {modern}")
    print(f"title     : {normalized_title}")
    print("-" * 56)
    print("不可变性演示:")
    demonstrate_immutability()
    print("=" * 56)
    print("✅ string_basics 运行成功")


if __name__ == "__main__":
    main()
