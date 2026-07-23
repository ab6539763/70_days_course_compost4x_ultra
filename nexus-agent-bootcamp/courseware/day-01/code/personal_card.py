#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人信息卡片生成器 — NexusAgent 训练营 Day 1 示例
模拟企业场景：为内部员工生成可打印的工牌信息摘要
"""

# 导入 sys 模块，用于读取命令行参数与退出码控制
import sys

# 定义员工姓名字符串变量，后续会参与格式化输出
employee_name = "张晓明"

# 定义员工工号，企业系统中唯一标识
employee_id = "SL-2026-0847"

# 定义所属部门名称
department = "智能体平台研发部"

# 定义岗位职级标题
job_title = "初级 Python 开发工程师"

# 定义入职日期字符串，格式为 ISO 风格 YYYY-MM-DD
hire_date = "2026-03-01"

# 定义办公地点楼层信息
office_location = "北京·中关村软件园 A3-1208"

# 定义直属经理姓名，用于工牌紧急联系人区
manager_name = "陈建国（Tech Lead）"

# 定义分隔线常量，全大写表示不可变配置
SEPARATOR_LINE = "=" * 48

# 定义副分隔线，视觉上弱于主分隔线
SUB_SEPARATOR = "-" * 48

# 使用 f-string 拼接多行卡片正文，\n 表示换行符
card_body = f"""
{SEPARATOR_LINE}
        智链科技 SmartLink · 员工信息卡
{SEPARATOR_LINE}
  姓名：{employee_name}
  工号：{employee_id}
  部门：{department}
  岗位：{job_title}
  入职：{hire_date}
  工位：{office_location}
  直属：{manager_name}
{SUB_SEPARATOR}
  系统账号：{employee_id.lower()}
  邮箱前缀：{employee_name[0]}.zhang@smartlink.cn
{SEPARATOR_LINE}
"""

# 定义欢迎语文案，强调训练营主线项目
welcome_message = (
    "欢迎加入 NexusAgent 项目组！"
    "今日目标：让 Python 在终端输出第一份「可交付」文本。"
)

# 主函数：组织程序入口逻辑，便于后续单元测试与复用
def main() -> None:
    # 向标准输出打印欢迎语
    print(welcome_message)
    # 打印空行，提升终端可读性
    print()
    # 打印完整卡片内容
    print(card_body)
    # 打印学习提示，引导学员修改变量观察变化
    print("提示：修改文件顶部变量后重新运行 python personal_card.py")


# Python 惯用入口守卫：仅在被直接执行时调用 main
if __name__ == "__main__":
    # 调用主函数
    main()
    # 以状态码 0 正常退出（显式写出便于学员理解退出语义）
    sys.exit(0)
