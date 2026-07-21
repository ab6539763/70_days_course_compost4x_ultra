"""Week 1 (Day 1-7) courseware definitions — Python 编程基础."""
from __future__ import annotations

import sys
from pathlib import Path

_PARENT = Path(__file__).resolve().parent.parent
if str(_PARENT) not in sys.path:
    sys.path.insert(0, str(_PARENT))

from generate_courseware import DayPlan  # noqa: E402

PHASE = "第一阶段:Python编程基础"
EPIC = "NEXUS-E1"

# ---------------------------------------------------------------------------
# Day 1
# ---------------------------------------------------------------------------

_DAY1_PERSONAL_CARD = '''#!/usr/bin/env python3
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

# 使用 f-string 拼接多行卡片正文，\\n 表示换行符
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
'''

_DAY1_ENV_CHECK = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发环境自检脚本 — 验证 Python 版本、编码与基本 IO 能力
企业场景：CI 流水线本地预检（pre-commit 前身）
"""

# 导入 platform 模块，读取操作系统与 Python 构建信息
import platform

# 导入 sys 模块，检查解释器版本与默认编码
import sys

# 导入 os 模块，检查环境变量与当前工作目录
import os

# 导入 locale 模块，检测系统区域与编码设置
import locale

# 导入 datetime 模块，为检查报告打上时间戳
from datetime import datetime

# 定义最低可接受的 Python 次版本号元组 (major, minor)
MIN_PYTHON = (3, 10)

# 定义检查项结果列表，每项为 (名称, 是否通过, 详情)
check_results: list[tuple[str, bool, str]] = []


def record_check(name: str, passed: bool, detail: str) -> None:
    """记录单项检查结果到全局列表。"""
    # 将三元组追加到结果列表
    check_results.append((name, passed, detail))


def check_python_version() -> None:
    """验证当前解释器版本是否满足训练营要求。"""
    # 读取当前版本的前两位 (major, minor)
    current = sys.version_info[:2]
    # 与最低版本比较，得到布尔值
    ok = current >= MIN_PYTHON
    # 格式化详情字符串，包含完整 version_info
    detail = f"当前 {current[0]}.{current[1]}，要求 >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]}"
    # 写入检查结果
    record_check("Python 版本", ok, detail)


def check_utf8_io() -> None:
    """验证标准输出能否正确处理中文（UTF-8）。"""
    # 测试字符串包含中文与 emoji，覆盖常见编码坑
    sample = "智链科技 NexusAgent 环境正常 ✅"
    try:
        # 尝试编码为 utf-8 字节再解码，模拟 IO 管道
        encoded = sample.encode("utf-8")
        decoded = encoded.decode("utf-8")
        # 比较往返后是否一致
        ok = decoded == sample
        detail = "UTF-8 编解码往返成功"
    except UnicodeError as exc:
        # 捕获编码异常并记录失败原因
        ok = False
        detail = f"编码异常: {exc}"
    record_check("UTF-8 中文 IO", ok, detail)


def check_working_directory() -> None:
    """确认当前工作目录可访问且包含预期课件路径片段。"""
    # 获取进程当前工作目录绝对路径
    cwd = os.getcwd()
    # 判断路径非空即视为可访问（极简校验，Day1 够用）
    ok = bool(cwd)
    detail = f"cwd={cwd}"
    record_check("工作目录", ok, detail)


def check_env_variables() -> None:
    """检查常用环境变量是否存在（非强制）。"""
    # 读取 PATH，开发者机器通常必有
    path_val = os.environ.get("PATH", "")
    # 有 PATH 即认为环境变量可读
    ok = len(path_val) > 0
    detail = f"PATH 长度={len(path_val)} 字符"
    record_check("环境变量 PATH", ok, detail)


def check_platform_info() -> None:
    """收集平台信息，便于讲师远程排查学员环境问题。"""
    # 拼接系统、版本、机器类型
    info = f"{platform.system()} {platform.release()} / {platform.machine()}"
    # 能读取即通过
    record_check("平台信息", True, info)


def render_report() -> str:
    """将检查结果渲染为可读文本报告。"""
    # 报告头部时间戳
    lines = [
        "=" * 50,
        "NexusAgent 开发环境自检报告",
        f"生成时间: {datetime.now().isoformat(timespec='seconds')}",
        "=" * 50,
    ]
    # 遍历每项检查，格式化 PASS/FAIL
    for name, passed, detail in check_results:
        status = "PASS" if passed else "FAIL"
        lines.append(f"[{status}] {name}: {detail}")
    # 统计失败数量
    failures = sum(1 for _, p, _ in check_results if not p)
    lines.append("-" * 50)
    lines.append(f"合计: {len(check_results)} 项, 失败 {failures} 项")
    # 用换行符连接各行
    return "\\n".join(lines)


def main() -> None:
    """按顺序执行全部检查并打印报告。"""
    check_python_version()
    check_utf8_io()
    check_working_directory()
    check_env_variables()
    check_platform_info()
    report = render_report()
    print(report)
    # 任一失败则退出码为 1，供脚本化调用
    has_failure = any(not p for _, p, _ in check_results)
    sys.exit(1 if has_failure else 0)


if __name__ == "__main__":
    main()
'''

DAY_01 = DayPlan(
    day=1,
    title="开发环境与第一行代码",
    phase=PHASE,
    epic=EPIC,
    jira_stories=[
        "NEXUS-E1-D01-S01",
        "NEXUS-E1-D01-S02",
        "NEXUS-E1-D01-S03",
    ],
    morning=[
        "09:00 站会：介绍 NexusAgent 70 天路线图与智链科技模拟组织架构",
        "09:30 安装 Python 3.10+、VS Code/Cursor、Git 基础配置",
        "10:30 终端入门：cd/ls/python3、路径与虚拟环境概念预习",
        "11:00 语法速览：变量、字符串、f-string、注释规范",
    ],
    afternoon=[
        "14:00 跟敲 personal_card.py：理解「可运行脚本」最小交付单元",
        "15:00 跟敲 env_check.py：建立「先自检再开发」的企业习惯",
        "16:00 代码 Review：命名规范 snake_case、文件头 docstring",
        "17:00 演示 Git 首次提交与 MR 流程（feature 分支）",
    ],
    evening=[
        "19:00 作业答疑：排查 Windows/macOS/Linux 环境差异",
        "20:00 预习 Day 2 运算符与字符串清洗场景",
        "20:30 学员互评：朗读各自卡片输出，互相找 typo",
    ],
    code_files={
        "personal_card.py": _DAY1_PERSONAL_CARD,
        "env_check.py": _DAY1_ENV_CHECK,
    },
    homework_desc="""\
**作业：定制你自己的「训练营学员证」**

1. 复制 `personal_card.py` 为 `homework/student_card.py`
2. 修改字段：姓名、学号（格式 NX-2026-XXXX）、班级、学习目标（一句话）
3. 新增函数 `build_footer()` 返回页脚字符串，包含生成日期（使用 `datetime.date.today()`）
4. 在 `main()` 中调用并打印页脚
5. 运行 `python homework/student_card.py` 并截图提交 MR

**验收标准**：脚本可运行、含中文无乱码、至少 2 个自定义函数、有类型注解。
""",
    homework_answer_hint="""\
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 学员证作业参考答案
from datetime import date


def build_footer() -> str:
  today = date.today().isoformat()
  return f"生成日期: {today} | NexusAgent Bootcamp Day 1"


def main() -> None:
  name = "李训练营"
  student_id = "NX-2026-0001"
  clazz = "70天零基础班 A 组"
  goal = "70 天内独立交付企业级 Agent 平台模块"
  print("=" * 40)
  print("智链科技 · 训练营学员证")
  print(f"姓名: {name}")
  print(f"学号: {student_id}")
  print(f"班级: {clazz}")
  print(f"目标: {goal}")
  print(build_footer())
  print("=" * 40)


if __name__ == "__main__":
  main()
```
""",
    architecture_mermaid="""flowchart LR
    DEV[开发者终端] --> PY[python3 解释器]
    PY --> CARD[personal_card.py]
    PY --> ENV[env_check.py]
    CARD --> STDOUT[标准输出 stdout]
    ENV --> EXIT[退出码 0/1]
    STDOUT --> MR[GitLab MR 截图附件]""",
    narration="""\
**陈工（Tech Lead）**：各位早上好，欢迎加入 NexusAgent 项目组。今天不追求写多复杂的代码，目标是三件事：环境能跑、第一行 Python 能输出中文、知道代码怎么提交到 GitLab。昨天产品林悦在 Jira 里挂了三个 Story，最核心的是「学员能在本地跑通示例脚本」——这是后面 69 天所有交付的门槛。

**林悦（产品经理）**：从用户视角，今天像「新员工入职打印工牌」。`personal_card.py` 就是最小可用产品：输入员工字段，输出可读卡片。字段设计别随便写，后面用户画像 Agent 会复用类似结构。

**小王（学员代表）**：我昨晚装好 Python，但 Windows 终端中文乱码怎么办？

**陈工**：下午 `env_check.py` 就是干这个的。企业里我们不会口头问「你环境好了吗」，而是用脚本自检，失败就标红退出码 1，CI 同理。今天先把地基打好，明天开始处理真实文本数据。
""",
    key_concepts=[
        "Python 解释器与 python3 命令",
        "变量赋值与动态类型",
        "f-string 格式化字符串",
        "模块导入 import",
        "if __name__ == '__main__' 入口守卫",
        "函数 def 与类型注解 -> None",
        "标准输出 print 与退出码 sys.exit",
        "UTF-8 编码与中文终端显示",
        "snake_case 命名规范",
        "docstring 文档字符串",
    ],
    platform_touches=[
        "Day 1 产出是 CLI 文本输出原型，对应 NexusAgent v0.1 最简用户可见界面",
        "env_check.py 模式将演进为 platform 的 scripts/preflight.py",
        "员工卡字段设计预演后续 UserProfile 数据结构",
    ],
)

# ---------------------------------------------------------------------------
# Day 2
# ---------------------------------------------------------------------------

_DAY2_TEXT_CLEANER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本清洗工具 text_cleaner.py
企业场景：客服工单、用户评论入库前的标准化预处理
"""

# 导入 re 模块，提供正则表达式能力
import re

# 导入 unicodedata，用于 Unicode 规范化（全角转半角等）
import unicodedata

# 导入 typing 中的类型别名辅助（仅注解，运行时不强制）
from typing import Iterable

# 定义默认需要剥离的空白字符集合
WHITESPACE_CHARS = " \\t\\n\\r\\f\\v"

# 定义常见中文标点映射表（全角 -> 半角或统一形式）
PUNCT_MAP = {
    "，": ",",
    "。": ".",
    "！": "!",
    "？": "?",
    "：": ":",
    "；": ";",
    "（": "(",
    "）": ")",
    "【": "[",
    "】": "]",
}


def normalize_unicode(text: str) -> str:
    """将文本做 NFC 规范化，减少同形异码问题。"""
    # NFKC 兼容分解再组合，常用于全角字母数字
    return unicodedata.normalize("NFKC", text)


def strip_edges(text: str) -> str:
    """去除首尾空白字符。"""
    # str.strip 可传入自定义字符集
    return text.strip(WHITESPACE_CHARS)


def collapse_internal_spaces(text: str) -> str:
    """将连续空白压缩为单个空格。"""
    # 正则 \\s+ 匹配任意空白 run
    return re.sub(r"\\s+", " ", text)


def replace_punctuation(text: str, mapping: dict[str, str] | None = None) -> str:
    """按映射表替换标点符号。"""
    # 若未传入映射则使用模块级默认表
    table = mapping if mapping is not None else PUNCT_MAP
    # 遍历映射逐项 replace（数据量小，Day2 足够）
    result = text
    for src, dst in table.items():
        result = result.replace(src, dst)
    return result


def remove_urls(text: str) -> str:
    """删除 http/https 链接，防止垃圾信息入库。"""
    # 简单 URL 正则，教学用途不追求 RFC 完整覆盖
    pattern = r"https?://\\S+"
    return re.sub(pattern, "[URL]", text)


def remove_mentions(text: str) -> str:
    """将 @用户名 替换为占位符。"""
    pattern = r"@\\w+"
    return re.sub(pattern, "@USER", text)


def mask_phone_numbers(text: str) -> str:
    """中国大陆手机号打码：保留前3后4。"""
    def _mask(match: re.Match[str]) -> str:
        # 提取匹配到的完整号码字符串
        phone = match.group(0)
        # 长度不足则原样返回
        if len(phone) < 7:
            return phone
        # 中间四位替换为星号
        return phone[:3] + "****" + phone[-4:]
    # 匹配 11 位 1 开头手机号
    return re.sub(r"1\\d{10}", _mask, text)


def clean_text(raw: str, *, mask_phone: bool = True) -> str:
    """
    管道式清洗：按固定顺序应用各子步骤。
    mask_phone 为关键字-only 参数，调用时必须写参数名。
    """
    # 空输入直接返回空串，避免后续无意义计算
    if not raw:
        return ""
    # 步骤 1：Unicode 规范化
    step = normalize_unicode(raw)
    # 步骤 2：去首尾空白
    step = strip_edges(step)
    # 步骤 3：压缩内部空白
    step = collapse_internal_spaces(step)
    # 步骤 4：标点统一
    step = replace_punctuation(step)
    # 步骤 5：URL 与 @ 处理
    step = remove_urls(step)
    step = remove_mentions(step)
    # 步骤 6：可选手机号脱敏
    if mask_phone:
        step = mask_phone_numbers(step)
    return step


def batch_clean(lines: Iterable[str]) -> list[str]:
    """批量清洗多行文本，返回新列表。"""
    # 列表推导式对每行调用 clean_text
    return [clean_text(line) for line in lines]


def word_count(text: str) -> dict[str, int]:
    """统计字符数、词数（空白分词）、行数。"""
    # 字符总数含标点
    chars = len(text)
    # split 默认按任意空白切分
    words = len(text.split()) if text else 0
    # 按换行分段
    lines = len(text.splitlines()) if text else 0
    # 返回结构化统计字典
    return {"chars": chars, "words": words, "lines": lines}


def demo() -> None:
    """演示入口：构造脏数据并打印清洗前后对比。"""
    dirty_samples = [
        "  你好，世界！  访问 https://smartlink.cn/docs  ",
        "@alice 我的手机号是13812345678，请回电。",
        "全角ＡＢＣ１２３　测试",
    ]
    print("=" * 56)
    print("text_cleaner 演示")
    print("=" * 56)
    for idx, raw in enumerate(dirty_samples, start=1):
        cleaned = clean_text(raw)
        stats = word_count(cleaned)
        print(f"[样本 {idx}] 原始: {raw!r}")
        print(f"[样本 {idx}] 清洗: {cleaned!r}")
        print(f"[样本 {idx}] 统计: {stats}")
        print("-" * 56)


def main() -> None:
    demo()


if __name__ == "__main__":
    main()
'''

DAY_02 = DayPlan(
    day=2,
    title="运算符与字符串",
    phase=PHASE,
    epic=EPIC,
    jira_stories=[
        "NEXUS-E1-D02-S01",
        "NEXUS-E1-D02-S02",
    ],
    morning=[
        "09:00 站会：回顾 Day1 MR，讲解字符串不可变特性",
        "09:30 算术/比较/逻辑运算符与优先级",
        "10:30 字符串方法：strip/split/join/replace/in",
        "11:00 切片与索引：正负下标、步长",
    ],
    afternoon=[
        "14:00 引入 re 模块：match/search/sub 基础",
        "14:45 跟敲 text_cleaner.py 管道式函数设计",
        "16:00 实操：为客服评论样本编写清洗规则",
        "17:00 Review：单一职责函数 vs 上帝函数",
    ],
    evening=[
        "19:00 作业：扩展清洗规则（邮箱打码）",
        "20:00 LeetCode 风格小练习：回文字符串判断",
        "20:45 阅读 Python 官方 str 文档索引",
    ],
    code_files={
        "text_cleaner.py": _DAY2_TEXT_CLEANER,
    },
    homework_desc="""\
**作业：扩展 text_cleaner**

1. 在 `homework/text_cleaner_hw.py` 中复制并扩展 `clean_text`
2. 新增 `mask_email(text)`：将 `user@domain.com` 转为 `u***@domain.com`
3. 新增 `extract_hashtags(text)`：返回文本中所有 `#话题` 列表（不含 #）
4. 编写 `assert` 自测至少 3 个用例
5. 提交 MR 并附终端运行截图
""",
    homework_answer_hint="""\
```python
import re

def mask_email(text: str) -> str:
  def repl(m: re.Match[str]) -> str:
    user, domain = m.group(1), m.group(2)
    masked = (user[0] + "***") if user else "***"
    return f"{masked}@{domain}"
  return re.sub(r"([\\w.+-]+)@([\\w.-]+)", repl, text)

def extract_hashtags(text: str) -> list[str]:
  return re.findall(r"#([\\w\\u4e00-\\u9fff]+)", text)

def clean_text(raw: str) -> str:
  step = raw.strip()
  step = mask_email(step)
  return step

assert extract_hashtags("关注 #NexusAgent #大模型") == ["NexusAgent", "大模型"]
assert "@" in mask_email("a@b.com")
print("homework tests passed")
```
""",
    architecture_mermaid="""flowchart TD
    RAW[原始文本] --> N1[normalize_unicode]
    N1 --> N2[strip_edges]
    N2 --> N3[collapse_spaces]
    N3 --> N4[replace_punctuation]
    N4 --> N5[remove_urls]
    N5 --> N6[mask_phone]
    N6 --> CLEAN[清洗结果]
    CLEAN --> STATS[word_count 统计]""",
    narration="""\
**林悦**：今天上午客服部发来一批用户反馈，里面全是表情、链接、手机号，直接进知识库会污染检索。Jira D02-S01 要求今天交付一个「文本清洗脚本」，能批量处理。

**陈工**：注意，别写一个 200 行的 `clean_all` 巨无霸函数。企业代码要管道化：每个函数只做一件事，方便单测，也方便以后把某一步换成 ML 模型。下午我们会用正则，别恐惧，先会用 `re.sub` 就够。

**小李（后端）**：字符串为什么不可变？我每次 `s.strip()` 好像改了原串？

**陈工**：`strip` 返回新对象，原串不变。这个特性关系到后面字典 key、缓存 key 的设计。今天把运算符和字符串吃透，明天流程控制写猜数字游戏就轻松了。
""",
    key_concepts=[
        "算术运算符 + - * / // % **",
        "比较运算符 == != < > <= >=",
        "逻辑运算符 and or not",
        "字符串不可变性与新对象",
        "str 方法 strip/split/join/replace",
        "切片 s[start:end:step]",
        "正则表达式 re.sub/re.findall",
        "Unicode 规范化 NFKC",
        "管道式数据处理",
        "关键字-only 参数 *",
    ],
    platform_touches=[
        "text_cleaner 是 NexusAgent 文档入库前清洗链路的教学原型",
        "mask_phone 规则将复用于日志脱敏中间件",
        "batch_clean 接口风格对齐后续 ETL 批处理任务",
    ],
)

# ---------------------------------------------------------------------------
# Day 3
# ---------------------------------------------------------------------------

_DAY3_GUESS_NUMBER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""猜数字游戏 — 练习 while、if、break 与随机数。"""
import random

SECRET_MIN = 1
SECRET_MAX = 100
MAX_ATTEMPTS = 7


def play_round() -> None:
    target = random.randint(SECRET_MIN, SECRET_MAX)
    attempts = 0
    print(f"我想了一个 {SECRET_MIN}-{SECRET_MAX} 的整数，你有 {MAX_ATTEMPTS} 次机会。")
    while attempts < MAX_ATTEMPTS:
        attempts += 1
        raw = input(f"第 {attempts} 次猜测: ").strip()
        if not raw.isdigit():
            print("请输入有效数字！")
            attempts -= 1
            continue
        guess = int(raw)
        if guess < target:
            print("太小了 ↑")
        elif guess > target:
            print("太大了 ↓")
        else:
            print(f"恭喜！{attempts} 次猜中！")
            return
    print(f"游戏结束，答案是 {target}")


def main() -> None:
    play_round()


if __name__ == "__main__":
    main()
'''

_DAY3_MULTIPLICATION_TABLE = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""九九乘法表 — 嵌套 for 循环与格式化对齐。"""
SIZE = 9


def print_table(size: int = SIZE) -> None:
    for i in range(1, size + 1):
        parts: list[str] = []
        for j in range(1, i + 1):
            parts.append(f"{j}×{i}={i*j:2d}")
        print("  ".join(parts))


def main() -> None:
    print_table()


if __name__ == "__main__":
    main()
'''

_DAY3_MENU_SYSTEM = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易菜单系统 — 流程控制综合练习
模拟 NexusAgent CLI 指令菜单雏形
"""
from __future__ import annotations

import sys


def show_banner() -> None:
    print("=" * 40)
    print("  NexusAgent CLI 菜单 (Day 3 教学版)")
    print("=" * 40)


def show_menu() -> None:
    print("1. 查看版本")
    print("2. 查看今日学习目标")
    print("3. 计算两数之和")
    print("0. 退出")


def handle_version() -> None:
    print("NexusAgent Bootcamp v0.1-day03")


def handle_goal() -> None:
    print("今日目标: 掌握 if/elif/else、while、for 与 break/continue")


def handle_add() -> None:
    a = input("输入整数 a: ").strip()
    b = input("输入整数 b: ").strip()
    if not (a.lstrip("-").isdigit() and b.lstrip("-").isdigit()):
        print("输入无效，请输入整数")
        return
    result = int(a) + int(b)
    print(f"结果: {result}")


def run_menu() -> None:
    actions = {
        "1": handle_version,
        "2": handle_goal,
        "3": handle_add,
    }
    show_banner()
    while True:
        show_menu()
        choice = input("请选择: ").strip()
        if choice == "0":
            print("再见！")
            break
        handler = actions.get(choice)
        if handler is None:
            print("无效选项，请重试")
            continue
        handler()
        print("-" * 40)


def main() -> None:
    try:
        run_menu()
    except KeyboardInterrupt:
        print("\\n用户中断，安全退出")
        sys.exit(0)


if __name__ == "__main__":
    main()
'''

DAY_03 = DayPlan(
    day=3,
    title="流程控制",
    phase=PHASE,
    epic=EPIC,
    jira_stories=[
        "NEXUS-E1-D03-S01",
        "NEXUS-E1-D03-S02",
        "NEXUS-E1-D03-S03",
    ],
    morning=[
        "09:00 站会：D02 清洗脚本已合并，今日进入控制流",
        "09:30 if/elif/else 分支与缩进规则（4 空格）",
        "10:30 while 循环、break/continue、无限循环陷阱",
        "11:00 for 循环与 range()、enumerate() 简介",
    ],
    afternoon=[
        "14:00 猜数字游戏：随机数与输入校验",
        "15:00 九九乘法表：嵌套循环与字符串对齐",
        "16:00 菜单系统：字典映射替代长 if-elif 链",
        "17:00 代码 Review：KeyboardInterrupt 优雅退出",
    ],
    evening=[
        "19:00 作业：为菜单增加「猜数字」子菜单项",
        "20:00 调试技巧：print 调试 vs 断点",
        "20:45 预习列表与 todo_manager 需求",
    ],
    code_files={
        "guess_number.py": _DAY3_GUESS_NUMBER,
        "multiplication_table.py": _DAY3_MULTIPLICATION_TABLE,
        "menu_system.py": _DAY3_MENU_SYSTEM,
    },
    homework_desc="""\
**作业：增强 menu_system.py**

1. 复制为 `homework/menu_extended.py`
2. 新增菜单项 `4. 启动猜数字`（复用 guess_number 逻辑或 import）
3. 新增菜单项 `5. 打印乘法表` 可输入 n（1-9）
4. 错误输入最多提示 3 次后返回主菜单（防止死循环）
5. 使用字典 `actions` 注册处理器，禁止超过 15 行的 elif 链
""",
    homework_answer_hint="""\
```python
import random

def play_guess() -> None:
  target = random.randint(1, 100)
  for i in range(1, 8):
    g = input("猜数字(1-100): ").strip()
    if not g.isdigit():
      print("无效"); continue
    n = int(g)
    if n == target:
      print(f"中了，{i}次"); return
    print("大" if n > target else "小")
  print(f"失败，答案{target}")

def print_table(n: int) -> None:
  for i in range(1, n + 1):
    print("  ".join(f"{j}×{i}={i*j}" for j in range(1, i + 1)))

actions = {"4": play_guess, "5": lambda: print_table(int(input("n=") or "9"))}
# 在 run_menu 的 actions 合并并处理无效输入计数
```
""",
    architecture_mermaid="""flowchart TD
    START[启动 menu_system] --> LOOP{while True}
    LOOP --> SHOW[show_menu]
    SHOW --> INPUT[用户输入 choice]
    INPUT -->|0| EXIT[退出]
    INPUT -->|1-3| DICT[actions 字典分发]
    DICT --> HANDLER[具体 handler]
    HANDLER --> LOOP""",
    narration="""\
**陈工**：流程控制是程序的「交通规则」。昨天字符串处理基本是直线执行，从今天开始代码会分叉、会循环。Jira 上三个 Story 分别对应三个可运行脚本，下午前必须都能独立跑通。

**林悦**：菜单系统不是玩具——NexusAgent CLI 以后就是「读指令 → 分发 → 执行」。今天用字典做 dispatch，别写 50 个 elif，那是维护地狱。

**小张**：`while True` 会不会让程序出不来？

**陈工**：所以要有明确的 `break` 条件和 `Ctrl+C` 处理。下午猜数字里加了输入校验和 `continue`，这是企业脚本防呆的第一课。写完记得自己故意输错几次，看看程序稳不稳。
""",
    key_concepts=[
        "if/elif/else 条件分支",
        "缩进块与 Python 语法",
        "while 循环与终止条件",
        "break 与 continue",
        "for 循环与 range",
        "嵌套循环时间复杂度直觉",
        "input() 与用户交互",
        "随机数 random.randint",
        "字典映射实现分发",
        "KeyboardInterrupt 异常处理",
    ],
    platform_touches=[
        "menu_system 是 NexusAgent CLI 交互模式的雏形",
        "actions 字典模式将用于注册 Agent 工具",
        "输入校验逻辑延续到后续 API 参数校验",
    ],
)

# ---------------------------------------------------------------------------
# Day 4
# ---------------------------------------------------------------------------

_DAY4_TODO_MANAGER = '''#!/usr/bin/env python3
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
        return "\\n".join(lines)


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
'''

DAY_04 = DayPlan(
    day=4,
    title="列表/元组/集合",
    phase=PHASE,
    epic=EPIC,
    jira_stories=[
        "NEXUS-E1-D04-S01",
        "NEXUS-E1-D04-S02",
    ],
    morning=[
        "09:00 站会：展示 Day3 菜单 MR，引入可变序列",
        "09:30 list 创建、索引、切片、append/extend/pop",
        "10:30 tuple 不可变与解包 *",
        "11:00 set 去重、交集并集差集",
    ],
    afternoon=[
        "14:00 列表推导式与生成器表达式预览",
        "14:45 跟敲 todo_manager：list + set 组合建模",
        "16:00 引入 dataclass 简化数据类",
        "17:00 Review：何时用 list vs set",
    ],
    evening=[
        "19:00 作业：待办支持优先级（用元组排序）",
        "20:00 练习：两列表找共同元素",
        "20:45 预习字典与 JSON",
    ],
    code_files={
        "todo_manager.py": _DAY4_TODO_MANAGER,
    },
    homework_desc="""\
**作业：待办优先级**

1. 扩展 `TodoItem` 增加字段 `priority: int`（1 高 - 5 低，默认 3）
2. 实现 `sort_by_priority()` 原地排序列表
3. 实现 `unique_tags()` 返回所有标签的集合
4. 编写 `demo_priority()` 添加 5 条不同优先级任务并打印排序结果
""",
    homework_answer_hint="""\
```python
@dataclass
class TodoItem:
  title: str
  priority: int = 3
  done: bool = False
  tags: set[str] = field(default_factory=set)

def sort_by_priority(self) -> None:
  self._items.sort(key=lambda x: x.priority)

def unique_tags(self) -> set[str]:
  result: set[str] = set()
  for item in self._items:
    result |= item.tags
  return result
```
""",
    architecture_mermaid="""flowchart LR
    MGR[TodoManager] --> LIST[list TodoItem]
    ITEM[TodoItem] --> TAGS[set tags]
    MGR --> ADD[add]
    MGR --> MARK[mark_done]
    MGR --> FILTER[list_by_tag]""",
    narration="""\
**林悦**：任务看板是项目管理的基本盘。今天用 Python 内置容器在内存里模拟 Jira 待办，不连数据库，但 CRUD 思路一致。

**陈工**：重点三个容器——list 有序可变、tuple 有序不可变、set 无序不重复。标签用 set，任务列表用 list。别把所有东西塞一个 list 里用魔法下标，用 dataclass 让字段可读。

**小王**：列表推导式什么时候用？

**陈工**：过滤转换一行能表达清楚就用，复杂逻辑还是 for 循环，可读性优先。下午 stats 和 list_by_tag 就是标准模式，背下来后面写 RAG 文档过滤会天天用。
""",
    key_concepts=[
        "list 可变序列与常用 API",
        "tuple 不可变与解包",
        "set 去重与集合运算",
        "索引与切片负下标",
        "列表推导式 [x for x in ...]",
        "in 成员运算符",
        "dataclass 数据类",
        "可选类型 Optional",
        "sort 与 sorted 区别",
        "类封装 _items 私有约定",
    ],
    platform_touches=[
        "TodoManager 建模预演 NexusAgent 任务队列",
        "tags 集合模式用于文档标签与权限组",
        "stats 接口风格对齐后续监控指标",
    ],
)

# ---------------------------------------------------------------------------
# Day 5
# ---------------------------------------------------------------------------

_DAY5_JSON_PARSER = '''#!/usr/bin/env python3
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
    path.write_text(text + "\\n", encoding="utf-8")


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
'''

DAY_05 = DayPlan(
    day=5,
    title="字典与JSON",
    phase=PHASE,
    epic=EPIC,
    jira_stories=[
        "NEXUS-E1-D05-S01",
        "NEXUS-E1-D05-S02",
    ],
    morning=[
        "09:00 站会：API 时代数据全是 JSON",
        "09:30 dict 创建、访问、get、keys/values/items",
        "10:30 嵌套 dict 与浅拷贝/copy",
        "11:00 json 模块 dumps/loads 与 ensure_ascii",
    ],
    afternoon=[
        "14:00 文件读写 Path.read_text/write_text",
        "14:45 跟敲 json_parser：校验与汇总",
        "16:00 错误处理：JSONDecodeError",
        "17:00 Review：配置与业务数据分离",
    ],
    evening=[
        "19:00 作业：解析课程表 JSON",
        "20:00 了解 JSON Schema 概念（预习）",
        "20:45 阅读 FastAPI 响应 JSON 示例（浏览）",
    ],
    code_files={
        "json_parser.py": _DAY5_JSON_PARSER,
    },
    homework_desc="""\
**作业：课程表 JSON**

1. 创建 `homework/schedule.json` 含至少 3 门课（name, day, hours）
2. 编写 `homework/schedule_loader.py` 读取并打印总学时
3. 实现 `find_by_day(schedule, day)` 返回当日课程列表
4. 非法 JSON 文件时打印友好错误，不崩溃
""",
    homework_answer_hint="""\
```python
import json
from pathlib import Path

def load_schedule(path: Path) -> list[dict]:
  try:
    return json.loads(path.read_text(encoding="utf-8"))
  except json.JSONDecodeError as e:
    print(f"JSON 解析失败: {e}")
    return []

def total_hours(courses: list[dict]) -> int:
  return sum(int(c.get("hours", 0)) for c in courses)

def find_by_day(courses: list[dict], day: int) -> list[dict]:
  return [c for c in courses if c.get("day") == day]
```
""",
    architecture_mermaid="""flowchart LR
    PY[Python dict/list] -->|dumps| STR[JSON 字符串]
    STR -->|loads| PY
    PY -->|save| FILE[.json 文件]
    FILE -->|load| PY
    PY --> VAL[validate_ticket]""",
    narration="""\
**陈工**：大模型应用开发天天跟 JSON 打交道——API 请求体、响应体、工具调用参数全是 JSON。dict 是 Python 里映射 JSON 的天然结构，今天必须熟练到肌肉记忆。

**林悦**：上午产品给了工单导出样例，下午 json_parser 要能校验、汇总、落盘。将来 NexusAgent 读 Jira Webhook 也是这个套路。

**小李**：`ensure_ascii=False` 是什么意思？

**陈工**：默认 dumps 会把中文转成 \\uXXXX，企业日志和配置文件可读性差。一律 False，文件编码 utf-8。嵌套访问别链式 `a['b']['c']` 炸 KeyError，用 get_nested 或 .get 渐进式取值。
""",
    key_concepts=[
        "dict 键值对与哈希表",
        "dict.get 默认值",
        "keys/values/items 遍历",
        "嵌套字典安全访问",
        "json.dumps 与 json.loads",
        "ensure_ascii=False 中文",
        "Path 读写 UTF-8 文件",
        "JSONDecodeError 异常",
        "数据校验返回 errors 列表",
        "按字段聚合统计",
    ],
    platform_touches=[
        "json_parser 对齐 NexusAgent 配置加载模块",
        "validate_ticket 预演 Webhook  payload 校验",
        "tickets_summary 类似看板状态统计 API",
    ],
)

# ---------------------------------------------------------------------------
# Day 6
# ---------------------------------------------------------------------------

_DAY6_STRING_UTILS = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""字符串工具模块 — 供重构演示的原始实现片段。"""
from __future__ import annotations

import re


def is_blank(text: str) -> bool:
    return text.strip() == ""


def truncate(text: str, max_len: int, suffix: str = "...") -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\\w\\s-]", "", text)
    text = re.sub(r"[-\\s]+", "-", text)
    return text.strip("-")
'''

_DAY6_VALIDATORS = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验工具 — 从菜单系统中抽离的输入验证逻辑。"""
from __future__ import annotations


def is_int_string(value: str) -> bool:
    value = value.strip()
    if value.startswith("-"):
        return value[1:].isdigit() if len(value) > 1 else False
    return value.isdigit()


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def require_non_empty(value: str, field_name: str = "字段") -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name}不能为空")
    return cleaned
'''

_DAY6_REFACTOR_DEMO = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
函数与重构综合演示 refactor_demo.py
展示：抽取函数、默认参数、*args/**kwargs、文档字符串
"""
from __future__ import annotations

from typing import Any, Callable

from string_utils import is_blank, slugify, truncate
from validators import clamp, is_int_string, require_non_empty


def greet(name: str, title: str = "同学") -> str:
    """生成问候语；title 为默认参数。"""
    safe_name = require_non_empty(name, "姓名")
    return f"你好，{title} {safe_name}！欢迎回到 NexusAgent 训练营。"


def apply_ops(values: list[int], *ops: Callable[[int], int]) -> list[int]:
    """对列表每个元素依次应用多个一元函数。"""
    result = list(values)
    for op in ops:
        result = [op(x) for x in result]
    return result


def build_user_record(**fields: Any) -> dict[str, Any]:
    """使用 **kwargs 构建用户记录字典。"""
    record = {"source": "bootcamp"}
    record.update(fields)
    return record


def format_profile(name: str, bio: str, max_bio: int = 80) -> str:
    """组合多个工具函数格式化个人简介。"""
    if is_blank(bio):
        bio = "（暂无简介）"
    short_bio = truncate(bio, max_bio)
    slug = slugify(name)
    return f"用户: {name} | slug: {slug} | 简介: {short_bio}"


def parse_menu_number(raw: str, low: int = 0, high: int = 9) -> int | None:
    """解析菜单数字输入，非法返回 None。"""
    if not is_int_string(raw):
        return None
    num = int(raw.strip())
    return clamp(num, low, high)


def demo() -> None:
    print(greet("张晓明"))
    print(greet("李雷", title="工程师"))
    doubled = apply_ops([1, 2, 3], lambda x: x * 2, lambda x: x + 1)
    print("apply_ops:", doubled)
    user = build_user_record(name="小王", role="学员", day=6)
    print("user record:", user)
    print(format_profile("Nexus Agent", "企业级智能体平台" * 5))
    print("menu parse:", parse_menu_number("42", 0, 9))


def main() -> None:
    demo()


if __name__ == "__main__":
    main()
'''

DAY_06 = DayPlan(
    day=6,
    title="函数",
    phase=PHASE,
    epic=EPIC,
    jira_stories=[
        "NEXUS-E1-D06-S01",
        "NEXUS-E1-D06-S02",
        "NEXUS-E1-D06-S03",
    ],
    morning=[
        "09:00 站会：Review Day5 JSON 作业，讨论代码重复问题",
        "09:30 函数定义、返回值、早返回 early return",
        "10:30 默认参数、关键字参数、*args/**kwargs",
        "11:00 作用域 LEGB 与命名空间预览",
    ],
    afternoon=[
        "14:00 从 menu_system 抽离 validators.py",
        "15:00 编写 string_utils.py 单一职责函数",
        "16:00 refactor_demo.py 组合调用与 docstring",
        "17:00 Review：DRY 原则与函数长度控制",
    ],
    evening=[
        "19:00 作业：为 json_parser 抽取 io_utils",
        "20:00 了解 lambda 适用边界",
        "20:45 预习 Week1 综合项目 contact_manager",
    ],
    code_files={
        "string_utils.py": _DAY6_STRING_UTILS,
        "validators.py": _DAY6_VALIDATORS,
        "refactor_demo.py": _DAY6_REFACTOR_DEMO,
    },
    homework_desc="""\
**作业：抽取 io_utils 模块**

1. 从 Day5 `json_parser` 抽出 `load_json_file` / `save_json_file` 到 `homework/io_utils.py`
2. 新增 `load_json_or_none(path)` 失败返回 None 并打印警告
3. `homework/test_io.py` 调用并断言往返一致
4. 原 json_parser 改为 from io_utils import ...（若在本目录运行需说明 PYTHONPATH）
""",
    homework_answer_hint="""\
```python
# homework/io_utils.py
import json
from pathlib import Path
from typing import Any

def load_json_file(path: Path) -> Any:
  return json.loads(path.read_text(encoding="utf-8"))

def save_json_file(path: Path, data: Any) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")

def load_json_or_none(path: Path) -> Any | None:
  try:
    return load_json_file(path)
  except (OSError, json.JSONDecodeError) as exc:
    print(f"[warn] 无法加载 {path}: {exc}")
    return None
```
""",
    architecture_mermaid="""flowchart TD
    DEMO[refactor_demo.py] --> SU[string_utils]
    DEMO --> VAL[validators]
    SU --> FUNCS[is_blank/truncate/slugify]
    VAL --> FUNCS2[is_int_string/clamp]""",
    narration="""\
**陈工**：Week1 前半段你们写了不少「能跑」的代码，今天专门治「乱」。函数不仅是语法，是团队分工的边界。Jira D06 要求把校验、字符串处理从业务脚本里撕出来。

**林悦**：产品不关心你几个文件，但关心改手机号校验规则时要不要改三个脚本。抽函数就是降低变更成本。

**小张**：`*args` 和 `**kwargs` 什么时候用？

**陈工**：需要透传或可变参数时用，别滥用。下午 `build_user_record(**fields)` 是典型配置型 API。每个函数加 docstring，参数含义写清楚，Code Review 省一半口水。明天 Week1 收官，把函数、dict、JSON、列表全串进通讯录项目。
""",
    key_concepts=[
        "def 函数定义与 return",
        "位置参数与关键字参数",
        "默认参数与可变默认陷阱",
        "*args 元组收集",
        "**kwargs 字典收集",
        "类型注解 Callable",
        "docstring 文档",
        "DRY 不要重复自己",
        "单一职责原则 SRP",
        "lambda 与高阶函数",
    ],
    platform_touches=[
        "validators 模块将并入 platform 输入校验层",
        "string_utils.slugify 用于生成文档 URL 片段",
        "模块拆分是 NexusAgent 包结构的基础",
    ],
)

# ---------------------------------------------------------------------------
# Day 7
# ---------------------------------------------------------------------------

_DAY7_CONTACT_MANAGER = '''#!/usr/bin/env python3
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
            json.dumps(data, ensure_ascii=False, indent=2) + "\\n",
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
        print("\\n中断退出，已尝试保存")
        repo.save()
        sys.exit(0)


if __name__ == "__main__":
    main()
'''

DAY_07 = DayPlan(
    day=7,
    title="周复习",
    phase=PHASE,
    epic=EPIC,
    jira_stories=[
        "NEXUS-E1-D07-S01",
        "NEXUS-E1-D07-S02",
    ],
    morning=[
        "09:00 Week1 复盘站会：知识点速查测验（口头）",
        "09:30 综合项目需求评审：通讯录 CRUD",
        "10:30 架构讲解：Entity / Repository / CLI 三层",
        "11:00 跟敲 contact_manager 数据模型与持久化",
    ],
    afternoon=[
        "14:00 完成 CLI 菜单与五项操作",
        "15:30 联调：增删改查 + 搜索 + 异常处理",
        "16:30 代码 Review：与 Day1-6 代码风格对齐",
        "17:00 合并 feature/week1-capstone 分支演示",
    ],
    evening=[
        "19:00 提交 Week1 总结 MR（模板由讲师提供）",
        "20:00 预习 Day8 文件操作与异常体系",
        "20:30 自习：修补本周薄弱点",
    ],
    code_files={
        "contact_manager.py": _DAY7_CONTACT_MANAGER,
    },
    homework_desc="""\
**作业：通讯录增强（Week1 收官）**

1. 在 `homework/contact_manager_plus.py` 基于课堂代码扩展
2. 新增「按标签过滤」菜单项
3. 新增「导出 CSV」到 `data/contacts_export.csv`（仅用 csv 标准库）
4. 删除前增加二次确认 `yes/no`
5. 编写 `homework/week1_quiz.md` 回答：list/dict/json/函数各一处本周应用场景

**加分项**：实现简单单元测试函数 `test_validate_contact()`
""",
    homework_answer_hint="""\
```python
import csv
from pathlib import Path

def filter_by_tag(repo, tag: str):
  return [c for c in repo.all() if tag in c.tags]

def export_csv(repo, path: Path) -> None:
  rows = repo.all()
  with path.open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "phone", "email", "company", "tags"])
    for c in rows:
      w.writerow([c.name, c.phone, c.email, c.company, ",".join(c.tags)])

def confirm_delete() -> bool:
  return input("确认删除? yes/no: ").strip().lower() == "yes"

def test_validate_contact():
  c = Contact("", "1")
  assert c.validate()
  c2 = Contact("a", "1", "bad-email")
  assert any("邮箱" in e for e in c2.validate())
```
""",
    architecture_mermaid="""flowchart TD
    CLI[ContactCLI] --> REPO[ContactRepository]
    REPO --> ENTITY[Contact dataclass]
    REPO --> JSON[(contacts.json)]
    CLI --> CRUD[增删改查搜索]
    ENTITY --> VAL[validate]""",
    narration="""\
**陈工**：Week1 最后一天，不上新语法，把前六天全部串起来。通讯录项目是迷你版 NexusAgent 用户管理：有实体、有仓储、有界面。上午讲完三层，下午必须能演示「添加 → 落盘 → 重启还在」。

**林悦**：验收标准我再说一遍：CRUD 完整、JSON 持久化、搜索能用、输入有错要提示人不能崩。这就是用户能感知的企业级质感。

**全班**：Day1 还不会装 Python，今天已经写 CRUD 了？

**陈工**：慢即是快。下周开始文件、异常、面向对象加深，再往后就是真 API 了。今晚作业加 CSV 导出，用标准库 csv 模块，别手写逗号——那是经典踩坑题。Week1 总结 MR 明早十点前交，我看谁把注释和异常处理偷懒了。
""",
    key_concepts=[
        "Week1 知识体系串联复盘",
        "dataclass 与 asdict 序列化",
        "Repository 仓储模式",
        "CRUD 完整生命周期",
        "JSON 文件持久化",
        "CLI 菜单与动作分发",
        "输入校验与 ValueError",
        "search 过滤与 any 生成器",
        "KeyboardInterrupt 安全保存",
        "三层架构 Entity-Repo-UI",
    ],
    platform_touches=[
        "contact_manager 是 NexusAgent 用户模块的教学替身",
        "ContactRepository 模式对齐后续 PostgreSQL DAO",
        "Week1 收官代码合并标记 platform v0.1-milestone",
    ],
)

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

DAYS_01_TO_07: list[DayPlan] = [
    DAY_01,
    DAY_02,
    DAY_03,
    DAY_04,
    DAY_05,
    DAY_06,
    DAY_07,
]
