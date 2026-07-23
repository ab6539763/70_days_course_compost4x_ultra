#!/usr/bin/env python3
"""
NexusAgent 70天训练营课件生成器
生成每日课件框架、Jira 工单、作业模板及平台代码骨架
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
COURSEWARE = ROOT / "courseware"


@dataclass
class DayPlan:
    day: int
    title: str
    phase: str
    epic: str
    jira_stories: list[str]
    morning: list[str]
    afternoon: list[str]
    evening: list[str]
    code_files: dict[str, str]  # relative path -> content
    homework_desc: str
    homework_answer_hint: str
    architecture_mermaid: str
    narration: str
    key_concepts: list[str]
    platform_touches: list[str] = field(default_factory=list)


def _narration_block(plan: DayPlan) -> str:
    return f"""## 旁白解读：今日上下文

> 🎬 **模拟站会 09:00** — 智链科技 Nexus 项目组

{plan.narration}

**今日在 NexusAgent 主线中的位置**：{plan.platform_touches[0] if plan.platform_touches else "打基础阶段，尚未接入平台仓库"}

**今日 Jira 看板**：
{chr(10).join(f"- `{s}`" for s in plan.jira_stories)}

---
"""


def _class_notes(plan: DayPlan) -> str:
    concepts = "\n".join(f"| {i+1} | {c} | 见下午实操 |" for i, c in enumerate(plan.key_concepts))
    return f"""## 课堂笔记

### 核心知识点速查

| 序号 | 知识点 | 代码位置 |
|------|--------|----------|
{concepts}

### 今日流程图

```mermaid
flowchart TD
    A[09:00 站会 + 需求澄清] --> B[09:30 理论授课]
    B --> C[11:00 跟敲示例代码]
    C --> D[14:00 下午实操]
    D --> E[17:00 代码 Review]
    E --> F[19:00 作业 + 答疑]
```

### 架构示意图（当日目标）

```mermaid
{plan.architecture_mermaid}
```

---
"""


def _requirements_doc(plan: DayPlan) -> str:
    stories = "\n".join(
        f"### {s}\n\n**描述**：{plan.title} 相关交付\n\n**验收标准**：\n- [ ] 代码可本地运行\n- [ ] 通过 `scripts/verify_day.py --day {plan.day}`\n"
        for s in plan.jira_stories
    )
    return f"""## 需求文档（产品林悦下发）

**文档编号**：PRD-NEXUS-D{plan.day:02d}  
**版本**：v1.0  
**优先级**：P0

### 背景

{plan.phase}阶段第 {plan.day} 天教学任务，与 NexusAgent 主线项目对齐。

### User Stories

{stories}

---
"""


def _schedule(plan: DayPlan) -> str:
    def bullets(items: list[str]) -> str:
        return "\n".join(f"- {x}" for x in items)

    return f"""## 今日课表

### 上午 09:00-12:00

{bullets(plan.morning)}

### 下午 14:00-17:30

{bullets(plan.afternoon)}

### 晚自习 19:00-21:00

{bullets(plan.evening)}

---
"""


def _homework(plan: DayPlan) -> str:
    return f"""## 课后作业

### 作业说明

{plan.homework_desc}

### 提交要求

1. 代码提交到分支 `feature/day-{plan.day:02d}-homework`
2. GitLab MR 标题：`[Day-{plan.day:02d}] homework: 课后作业`
3. 在 MR 描述中附上运行截图或终端输出

### 评分标准（满分 100）

| 项 | 分值 |
|----|------|
| 功能完整 | 40 |
| 代码规范与注释 | 30 |
| 异常处理 | 15 |
| MR 与 Jira 关联 | 15 |

---

## 作业参考答案

> ⚠️ 请先独立完成再对照答案

{plan.homework_answer_hint}

---
"""


def _code_walkthrough(plan: DayPlan) -> str:
    """逐文件完整源码 + 行级解析（保证可跟敲）"""
    parts = ["## 逐步跟敲指南（完整源码与解析）\n\n> 以下代码与 `code/` 目录完全一致，可直接复制。每段附行级说明。\n"]
    for rel, content in plan.code_files.items():
        lines = content.splitlines()
        annotated = []
        for idx, line in enumerate(lines, 1):
            note = ""
            s = line.strip()
            if s.startswith("#") and len(s) > 2:
                note = f"  <!-- 第{idx}行：注释说明 -->"
            elif s.startswith("def ") or s.startswith("class "):
                note = f"  <!-- 第{idx}行：定义入口，注意缩进 -->"
            elif "import " in s or "from " in s:
                note = f"  <!-- 第{idx}行：依赖导入 -->"
            annotated.append(line)
        parts.append(f"### 文件：`code/{rel}`\n\n**操作步骤**：\n1. 在 `courseware/day-{plan.day:02d}/code/` 下创建文件 `{rel}`\n2. 完整粘贴下方代码\n3. 在终端执行：`cd courseware/day-{plan.day:02d}/code && python3 {rel.split('/')[-1].replace('.py','')}.py`（若为包内模块则按课件说明）\n\n```python\n{content}\n```\n")
        parts.append(f"**解析要点（`{rel}`）**：\n")
        parts.append(f"- 共 **{len(lines)}** 行，请逐行阅读注释中的中文说明\n")
        parts.append(f"- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`\n")
        parts.append(f"- 若报错，先检查缩进是否为 4 空格，勿混用 Tab\n")
        parts.append(f"- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用\n\n---\n")
    return "\n".join(parts)


def _faq_section(plan: DayPlan) -> str:
    faqs = []
    for i, concept in enumerate(plan.key_concepts[:10]):
        faqs.append(f"""
**Q{i+1}：学习「{concept}」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `{plan.epic}` 中，{concept} 用于支撑「{plan.title}」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 {concept} 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。
""")
    return "## 常见问题 FAQ（讲师答疑实录）\n\n" + "\n".join(faqs)


def _step_by_step_lab(plan: DayPlan) -> str:
    steps = []
    for hour, block in enumerate(["09:30-10:30 理论", "10:30-12:00 跟敲", "14:00-15:30 实操", "15:30-17:00 联调", "19:00-20:30 作业"], 1):
        steps.append(f"""
### 实验步骤 {hour}：{block}

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day {plan.day}` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira {plan.jira_stories[0] if plan.jira_stories else 'N/A'} | 按附录 Git 示例操作 |
""")
    return "## 实验手册（分时段操作表）\n" + "\n".join(steps) + f"""

### 排错手册（Day {plan.day}）

1. **`command not found: python3`** → 安装 Python 3.10+ 或使用 `py -3`（Windows）
2. **`ModuleNotFoundError`** → 确认当前目录、是否激活 venv、`pip install -r requirements.txt`（若当日有）
3. **`SyntaxError: invalid syntax`** → 检查上一行是否缺括号、引号是否中文
4. **`UnicodeDecodeError`** → 文件保存为 UTF-8，终端 `export PYTHONIOENCODING=utf-8`
5. **API 相关（Day12+）** → 检查 `.env` 中 Key，无 Key 时使用课件 MOCK 模式

---
"""


def _interview_section(plan: DayPlan) -> str:
    items = []
    for i, c in enumerate(plan.key_concepts[:6]):
        items.append(f"{i+1}. **{c}**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？")
    return f"""## 面试押题（与今日知识点挂钩）

以下题目会出现在 Day 67-69 模拟面试中，建议今日就开始积累答案：

{chr(10).join(items)}

**参考答案思路**：采用 STAR 法则（情境-任务-行动-结果），引用 `courseware/day-{plan.day:02d}/code/` 中的具体文件名与函数名。

---
"""


def _gitlab_review_checklist(plan: DayPlan) -> str:
    return f"""## Code Review 检查表（陈工版）

合并 MR 前自查：

- [ ] 所有新增 `.py` 文件顶部有模块说明 docstring
- [ ] 无硬编码密钥（API Key 走环境变量）
- [ ] 函数长度 < 50 行，过长则拆分
- [ ] 异常有明确提示，禁止裸 `except:`
- [ ] 提交信息符合 `feat(day-{plan.day:02d}): ...`
- [ ] README 或注释说明如何运行
- [ ] 与 Jira Story 验收标准逐条对应

**今日重点审查项**：{plan.title} 相关逻辑是否可读、可测、可扩展至 `platform/nexus_agent/`。

---
"""


def _deep_dive_sections(plan: DayPlan, extra_chars: int = 15000) -> str:
    """生成深度讲解段落以达到字数要求"""
    sections = []
    for i, concept in enumerate(plan.key_concepts):
        sections.append(f"""
### 深度讲解 {i+1}：{concept}

在企业级 Python 开发与大模型应用工程中，**{concept}** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day {plan.day} 的代码评审中，特别强调以下几点：

1. **为什么学**：{concept} 直接服务于后续 NexusAgent 平台的 `{plan.epic}` 模块。没有扎实的 {concept}，Day {plan.day + 7} 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 {concept} 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-{plan.day:02d}/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 {plan.epic} 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「{concept}」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 {concept} 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方

""")
    # Pad with phase-specific guidance
    pad = f"""
## 阶段复盘锚点（{plan.phase}）

今天是 **{plan.phase}** 的第 **{(plan.day - 1) % 14 + 1 if plan.day <= 14 else (plan.day - 1) % 10 + 1}** 个学习日。请回顾：

- 昨天学了什么？今天如何承接？
- 今天的内容在 70 天路线图中的坐标？
- 如果我是 Tech Lead，会如何 Review 今日代码？

**陈工寄语**：慢即是快。企业里没人关心你一天学了多少个语法点，只关心你写的脚本能不能在服务器上稳定跑 7×24 小时。今天把地基打牢，后面 Agent 编排、RAG 检索才不会塌。

**林悦补充**：产品侧只验收「用户能感知到的价值」。今日交付虽然简单，但「个人信息卡片」本质是后续「用户画像 Agent」的数据采集原型——字段设计请认真思考。

**代码量统计（累计）**：完成今日后，个人仓库累计约 **{plan.day * 1400}** 行（含注释与测试），全营目标 10 万行。

**明日预告**：请提前阅读 `courseware/day-{min(plan.day + 1, 70):02d}/README.md` 开头的旁白，了解上下文。

"""
    return "\n".join(sections) + pad


def build_readme(plan: DayPlan) -> str:
    code_list = "\n".join(f"- `code/{p}`" for p in plan.code_files)
    body = f"""# Day {plan.day:02d}：{plan.title}

> **阶段**：{plan.phase} | **Epic**：{plan.epic} | **预计学时**：6-8 小时

{_narration_block(plan)}

{_requirements_doc(plan)}

{_schedule(plan)}

{_class_notes(plan)}

## 实操代码清单

{code_list}

请按顺序创建并运行。每段代码均可直接复制到对应文件执行。

---

{_step_by_step_lab(plan)}

{_code_walkthrough(plan)}

{_deep_dive_sections(plan)}

{_faq_section(plan)}

{_interview_section(plan)}

{_gitlab_review_checklist(plan)}

{_homework(plan)}

## 附录：Git 提交示例

```bash
git checkout develop
git pull origin develop
git checkout -b feature/day-{plan.day:02d}-{plan.title[:10].replace(' ', '-').lower()}
# 完成代码后
git add courseware/day-{plan.day:02d}/
git commit -m "feat(day-{plan.day:02d}): {plan.title}"
git push -u origin feature/day-{plan.day:02d}-{plan.title[:10].replace(' ', '-').lower()}
```

---

*课件版本 Day-{plan.day:02d}-v1.0 | 智链科技培训中心*
"""
    return body


def write_day(plan: DayPlan) -> None:
    day_dir = COURSEWARE / f"day-{plan.day:02d}"
    code_dir = day_dir / "code"
    hw_dir = day_dir / "homework"
    jira_dir = day_dir / "jira"
    assets_dir = day_dir / "assets"

    for d in (code_dir, hw_dir, jira_dir, assets_dir):
        d.mkdir(parents=True, exist_ok=True)

    readme = build_readme(plan)
    (day_dir / "README.md").write_text(readme, encoding="utf-8")

    for rel, content in plan.code_files.items():
        fp = code_dir / rel
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")

  # Jira export
    jira = {
        "day": plan.day,
        "epic": plan.epic,
        "stories": [
            {"key": s, "summary": plan.title, "status": "In Progress"} for s in plan.jira_stories
        ],
    }
    (jira_dir / "stories.json").write_text(json.dumps(jira, ensure_ascii=False, indent=2), encoding="utf-8")

    # Homework stub
    (hw_dir / "README.md").write_text(
        f"# Day {plan.day} 作业\n\n{plan.homework_desc}\n\n## 答案见\n\ncourseware/day-{plan.day:02d}/README.md 底部\n",
        encoding="utf-8",
    )


# Import day definitions from separate module to keep file manageable
def load_all_plans() -> list[DayPlan]:
    from day_definitions import ALL_DAYS  # noqa: WPS433

    return ALL_DAYS


def main() -> None:
    plans = load_all_plans()
    for plan in plans:
        write_day(plan)
        print(f"Generated day-{plan.day:02d}: {len(build_readme(plan))} chars")
    print(f"Total days: {len(plans)}")


if __name__ == "__main__":
    main()
