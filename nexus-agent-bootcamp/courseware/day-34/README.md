# Day 34：Ragas 评估

> **阶段**：Phase 3：LangChain RAG 知识库 | **Epic**：NEXUS-E3 | **预计学时**：6-8 小时

## 旁白解读：今日上下文

> 🎬 **模拟站会 09:00** — 智链科技 Nexus 项目组

**林悦**：没有 Ragas 报告不准上线。**陈工**：faithfulness 低就是幻觉重灾区。

**今日在 NexusAgent 主线中的位置**：Nexus RAG 质量门禁指标

**今日 Jira 看板**：
- `NEXUS-341`
- `NEXUS-342`

---


## 需求文档（产品林悦下发）

**文档编号**：PRD-NEXUS-D34  
**版本**：v1.0  
**优先级**：P0

### 背景

Phase 3：LangChain RAG 知识库阶段第 34 天教学任务，与 NexusAgent 主线项目对齐。

### User Stories

### NEXUS-341

**描述**：Ragas 评估 相关交付

**验收标准**：
- [ ] 代码可本地运行
- [ ] 通过 `scripts/verify_day.py --day 34`

### NEXUS-342

**描述**：Ragas 评估 相关交付

**验收标准**：
- [ ] 代码可本地运行
- [ ] 通过 `scripts/verify_day.py --day 34`


---


## 今日课表

### 上午 09:00-12:00

- 09:00 RAG 评估指标
- 10:00 faithfulness / answer_relevancy
- 11:00 Ragas 框架

### 下午 14:00-17:30

- 14:00 构建评估数据集
- 16:00 跑 Ragas 评测
- 17:00 解读报告

### 晚自习 19:00-21:00

- 19:00 作业：5 条人工标注
- 20:00 预习 LlamaIndex

---


## 课堂笔记

### 核心知识点速查

| 序号 | 知识点 | 代码位置 |
|------|--------|----------|
| 1 | Ragas | 见下午实操 |
| 2 | faithfulness | 见下午实操 |
| 3 | answer_relevancy | 见下午实操 |
| 4 | 评估数据集 | 见下午实操 |

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
flowchart LR\n  RAG --> PRED[预测]\n  GT[标注] --> RAGAS --> METRICS[指标]
```

---


## 实操代码清单

- `code/ragas_eval.py`
- `code/eval_dataset.json`
- `code/run_ragas.py`

请按顺序创建并运行。每段代码均可直接复制到对应文件执行。

---

## 实验手册（分时段操作表）

### 实验步骤 1：09:30-10:30 理论

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 34` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-341 | 按附录 Git 示例操作 |


### 实验步骤 2：10:30-12:00 跟敲

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 34` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-341 | 按附录 Git 示例操作 |


### 实验步骤 3：14:00-15:30 实操

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 34` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-341 | 按附录 Git 示例操作 |


### 实验步骤 4：15:30-17:00 联调

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 34` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-341 | 按附录 Git 示例操作 |


### 实验步骤 5：19:00-20:30 作业

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 34` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-341 | 按附录 Git 示例操作 |


### 排错手册（Day 34）

1. **`command not found: python3`** → 安装 Python 3.10+ 或使用 `py -3`（Windows）
2. **`ModuleNotFoundError`** → 确认当前目录、是否激活 venv、`pip install -r requirements.txt`（若当日有）
3. **`SyntaxError: invalid syntax`** → 检查上一行是否缺括号、引号是否中文
4. **`UnicodeDecodeError`** → 文件保存为 UTF-8，终端 `export PYTHONIOENCODING=utf-8`
5. **API 相关（Day12+）** → 检查 `.env` 中 Key，无 Key 时使用课件 MOCK 模式

---


## 逐步跟敲指南（完整源码与解析）

> 以下代码与 `code/` 目录完全一致，可直接复制。每段附行级说明。

### 文件：`code/ragas_eval.py`

**操作步骤**：
1. 在 `courseware/day-34/code/` 下创建文件 `ragas_eval.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-34/code && python3 ragas_eval.py`（若为包内模块则按课件说明）

```python
#!/usr/bin/env python3
"""Day 34: Ragas 评估（可选依赖，无则 mock）"""
from dataclasses import dataclass

@dataclass
class RagSample:
  question: str
  answer: str
  contexts: list[str]
  ground_truth: str

def faithfulness(answer: str, contexts: list[str]) -> float:
  # 答案是否可由上下文推出
  ctx = " ".join(contexts)
  overlap = sum(1 for w in answer.split() if w in ctx)
  return min(overlap / max(len(answer.split()), 1), 1.0)

def answer_relevancy(answer: str, question: str) -> float:
  overlap = sum(1 for w in question.split() if w in answer)
  return min(overlap / max(len(question.split()), 1), 1.0)

if __name__ == "__main__":
  s = RagSample("年假几天", "5天年假", ["工作满一年享5天年假"], "5天")
  print("faithfulness:", faithfulness(s.answer, s.contexts))
  print("relevancy:", answer_relevancy(s.answer, s.question))

```

**解析要点（`ragas_eval.py`）**：

- 共 **25** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/eval_dataset.json`

**操作步骤**：
1. 在 `courseware/day-34/code/` 下创建文件 `eval_dataset.json`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-34/code && python3 eval_dataset.json.py`（若为包内模块则按课件说明）

```python
[
  {"question": "年假有几天", "ground_truth": "5天", "contexts": ["工作满一年享5天年假"]},
  {"question": "报销期限", "ground_truth": "30日内", "contexts": ["差旅费30日内提交"]}
]

```

**解析要点（`eval_dataset.json`）**：

- 共 **4** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/run_ragas.py`

**操作步骤**：
1. 在 `courseware/day-34/code/` 下创建文件 `run_ragas.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-34/code && python3 run_ragas.py`（若为包内模块则按课件说明）

```python
#!/usr/bin/env python3
"""Day 34: 批量评估脚本"""
import json
from pathlib import Path
from ragas_eval import RagSample, faithfulness, answer_relevancy

def run_eval() -> None:
  data = json.loads(Path("eval_dataset.json").read_text(encoding="utf-8"))
  for row in data:
    ans = row.get("predicted", row["ground_truth"])
    f = faithfulness(ans, row["contexts"])
    r = answer_relevancy(ans, row["question"])
    print(row["question"], f"F={f:.2f} R={r:.2f}")

if __name__ == "__main__":
  run_eval()

```

**解析要点（`run_ragas.py`）**：

- 共 **16** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---



### 深度讲解 1：Ragas

在企业级 Python 开发与大模型应用工程中，**Ragas** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 34 的代码评审中，特别强调以下几点：

1. **为什么学**：Ragas 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 Ragas，Day 41 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 Ragas 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-34/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「Ragas」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 Ragas 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 2：faithfulness

在企业级 Python 开发与大模型应用工程中，**faithfulness** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 34 的代码评审中，特别强调以下几点：

1. **为什么学**：faithfulness 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 faithfulness，Day 41 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 faithfulness 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-34/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「faithfulness」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 faithfulness 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 3：answer_relevancy

在企业级 Python 开发与大模型应用工程中，**answer_relevancy** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 34 的代码评审中，特别强调以下几点：

1. **为什么学**：answer_relevancy 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 answer_relevancy，Day 41 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 answer_relevancy 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-34/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「answer_relevancy」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 answer_relevancy 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 4：评估数据集

在企业级 Python 开发与大模型应用工程中，**评估数据集** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 34 的代码评审中，特别强调以下几点：

1. **为什么学**：评估数据集 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 评估数据集，Day 41 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 评估数据集 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-34/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「评估数据集」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 评估数据集 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方


## 阶段复盘锚点（Phase 3：LangChain RAG 知识库）

今天是 **Phase 3：LangChain RAG 知识库** 的第 **4** 个学习日。请回顾：

- 昨天学了什么？今天如何承接？
- 今天的内容在 70 天路线图中的坐标？
- 如果我是 Tech Lead，会如何 Review 今日代码？

**陈工寄语**：慢即是快。企业里没人关心你一天学了多少个语法点，只关心你写的脚本能不能在服务器上稳定跑 7×24 小时。今天把地基打牢，后面 Agent 编排、RAG 检索才不会塌。

**林悦补充**：产品侧只验收「用户能感知到的价值」。今日交付虽然简单，但「个人信息卡片」本质是后续「用户画像 Agent」的数据采集原型——字段设计请认真思考。

**代码量统计（累计）**：完成今日后，个人仓库累计约 **47600** 行（含注释与测试），全营目标 10 万行。

**明日预告**：请提前阅读 `courseware/day-35/README.md` 开头的旁白，了解上下文。



## 常见问题 FAQ（讲师答疑实录）


**Q1：学习「Ragas」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，Ragas 用于支撑「Ragas 评估」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 Ragas 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q2：学习「faithfulness」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，faithfulness 用于支撑「Ragas 评估」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 faithfulness 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q3：学习「answer_relevancy」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，answer_relevancy 用于支撑「Ragas 评估」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 answer_relevancy 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q4：学习「评估数据集」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，评估数据集 用于支撑「Ragas 评估」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 评估数据集 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


## 面试押题（与今日知识点挂钩）

以下题目会出现在 Day 67-69 模拟面试中，建议今日就开始积累答案：

1. **Ragas**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
2. **faithfulness**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
3. **answer_relevancy**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
4. **评估数据集**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？

**参考答案思路**：采用 STAR 法则（情境-任务-行动-结果），引用 `courseware/day-34/code/` 中的具体文件名与函数名。

---


## Code Review 检查表（陈工版）

合并 MR 前自查：

- [ ] 所有新增 `.py` 文件顶部有模块说明 docstring
- [ ] 无硬编码密钥（API Key 走环境变量）
- [ ] 函数长度 < 50 行，过长则拆分
- [ ] 异常有明确提示，禁止裸 `except:`
- [ ] 提交信息符合 `feat(day-34): ...`
- [ ] README 或注释说明如何运行
- [ ] 与 Jira Story 验收标准逐条对应

**今日重点审查项**：Ragas 评估 相关逻辑是否可读、可测、可扩展至 `platform/nexus_agent/`。

---


## 课后作业

### 作业说明

扩展 eval_dataset.json 至 10 条，接入真实 RAG 输出跑评估。

### 提交要求

1. 代码提交到分支 `feature/day-34-homework`
2. GitLab MR 标题：`[Day-34] homework: 课后作业`
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

对每条 question 调用 rag_pipeline，将 answer 写入 predicted 字段。

---


## 附录：Git 提交示例

```bash
git checkout develop
git pull origin develop
git checkout -b feature/day-34-ragas-评估
# 完成代码后
git add courseware/day-34/
git commit -m "feat(day-34): Ragas 评估"
git push -u origin feature/day-34-ragas-评估
```

---

*课件版本 Day-34-v1.0 | 智链科技培训中心*
