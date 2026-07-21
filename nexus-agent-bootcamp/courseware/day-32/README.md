# Day 32：高级 RAG（上）

> **阶段**：Phase 3：LangChain RAG 知识库 | **Epic**：NEXUS-E3 | **预计学时**：6-8 小时

## 旁白解读：今日上下文

> 🎬 **模拟站会 09:00** — 智链科技 Nexus 项目组

**陈工**：用户问法千奇百怪，Multi-Query 是性价比最高的高级技巧。

**今日在 NexusAgent 主线中的位置**：Nexus 检索层支持多查询扩展

**今日 Jira 看板**：
- `NEXUS-321`
- `NEXUS-322`

---


## 需求文档（产品林悦下发）

**文档编号**：PRD-NEXUS-D32  
**版本**：v1.0  
**优先级**：P0

### 背景

Phase 3：LangChain RAG 知识库阶段第 32 天教学任务，与 NexusAgent 主线项目对齐。

### User Stories

### NEXUS-321

**描述**：高级 RAG（上） 相关交付

**验收标准**：
- [ ] 代码可本地运行
- [ ] 通过 `scripts/verify_day.py --day 32`

### NEXUS-322

**描述**：高级 RAG（上） 相关交付

**验收标准**：
- [ ] 代码可本地运行
- [ ] 通过 `scripts/verify_day.py --day 32`


---


## 今日课表

### 上午 09:00-12:00

- 09:00 Query Transformation
- 10:00 Multi-Query Retriever
- 11:00 HyDE 概念

### 下午 14:00-17:30

- 14:00 查询扩展实现
- 16:00 Reranker 接入
- 17:00 效果对比

### 晚自习 19:00-21:00

- 19:00 作业：Multi-Query
- 20:00 预习混合检索

---


## 课堂笔记

### 核心知识点速查

| 序号 | 知识点 | 代码位置 |
|------|--------|----------|
| 1 | Query Expansion | 见下午实操 |
| 2 | Multi-Query | 见下午实操 |
| 3 | Reranker | 见下午实操 |
| 4 | HyDE | 见下午实操 |

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
flowchart TD\n  Q --> EXP[查询扩展] --> Q1 Q2 Q3\n  Q1 --> RET --> MERGE --> RERANK
```

---


## 实操代码清单

- `code/query_expansion.py`
- `code/reranker.py`
- `code/hyde_stub.py`

请按顺序创建并运行。每段代码均可直接复制到对应文件执行。

---

## 实验手册（分时段操作表）

### 实验步骤 1：09:30-10:30 理论

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 32` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-321 | 按附录 Git 示例操作 |


### 实验步骤 2：10:30-12:00 跟敲

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 32` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-321 | 按附录 Git 示例操作 |


### 实验步骤 3：14:00-15:30 实操

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 32` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-321 | 按附录 Git 示例操作 |


### 实验步骤 4：15:30-17:00 联调

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 32` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-321 | 按附录 Git 示例操作 |


### 实验步骤 5：19:00-20:30 作业

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 32` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-321 | 按附录 Git 示例操作 |


### 排错手册（Day 32）

1. **`command not found: python3`** → 安装 Python 3.10+ 或使用 `py -3`（Windows）
2. **`ModuleNotFoundError`** → 确认当前目录、是否激活 venv、`pip install -r requirements.txt`（若当日有）
3. **`SyntaxError: invalid syntax`** → 检查上一行是否缺括号、引号是否中文
4. **`UnicodeDecodeError`** → 文件保存为 UTF-8，终端 `export PYTHONIOENCODING=utf-8`
5. **API 相关（Day12+）** → 检查 `.env` 中 Key，无 Key 时使用课件 MOCK 模式

---


## 逐步跟敲指南（完整源码与解析）

> 以下代码与 `code/` 目录完全一致，可直接复制。每段附行级说明。

### 文件：`code/query_expansion.py`

**操作步骤**：
1. 在 `courseware/day-32/code/` 下创建文件 `query_expansion.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-32/code && python3 query_expansion.py`（若为包内模块则按课件说明）

```python
#!/usr/bin/env python3
"""Day 32: 多查询扩展检索"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
  "将用户问题改写成 3 个不同表述的检索查询，每行一个：\n{question}"
)
llm = ChatOpenAI(
  model="deepseek-chat",
  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
expand_chain = prompt | llm | StrOutputParser()

def multi_query(question: str) -> list[str]:
  text = expand_chain.invoke({"question": question})
  return [line.strip() for line in text.splitlines() if line.strip()][:3]

if __name__ == "__main__":
  print(multi_query("员工年假怎么算？"))

```

**解析要点（`query_expansion.py`）**：

- 共 **23** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/reranker.py`

**操作步骤**：
1. 在 `courseware/day-32/code/` 下创建文件 `reranker.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-32/code && python3 reranker.py`（若为包内模块则按课件说明）

```python
#!/usr/bin/env python3
"""Day 32: 简易 Reranker — 按关键词重叠重排"""
from dataclasses import dataclass

@dataclass
class Doc:
  text: str
  score: float = 0.0

def rerank(query: str, docs: list[Doc]) -> list[Doc]:
  q_tokens = set(query)
  for d in docs:
    d.score = sum(1 for c in q_tokens if c in d.text) / max(len(q_tokens), 1)
  return sorted(docs, key=lambda x: x.score, reverse=True)

if __name__ == "__main__":
  docs = [Doc("年假 5 天"), Doc("报销发票"), Doc("考勤打卡")]
  for d in rerank("年假", docs):
    print(d.score, d.text)

```

**解析要点（`reranker.py`）**：

- 共 **19** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/hyde_stub.py`

**操作步骤**：
1. 在 `courseware/day-32/code/` 下创建文件 `hyde_stub.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-32/code && python3 hyde_stub.py`（若为包内模块则按课件说明）

```python
#!/usr/bin/env python3
"""Day 32: HyDE — 先生成假设文档再检索（占位）"""
import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
  model="deepseek-chat",
  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)

def hyde_query(question: str) -> str:
  # 生成一段「假设性答案」作为检索 query
  return f"假设文档：关于「{question}」的标准解答段落..."

if __name__ == "__main__":
  print(hyde_query("远程办公政策"))

```

**解析要点（`hyde_stub.py`）**：

- 共 **17** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---



### 深度讲解 1：Query Expansion

在企业级 Python 开发与大模型应用工程中，**Query Expansion** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 32 的代码评审中，特别强调以下几点：

1. **为什么学**：Query Expansion 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 Query Expansion，Day 39 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 Query Expansion 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-32/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「Query Expansion」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 Query Expansion 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 2：Multi-Query

在企业级 Python 开发与大模型应用工程中，**Multi-Query** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 32 的代码评审中，特别强调以下几点：

1. **为什么学**：Multi-Query 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 Multi-Query，Day 39 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 Multi-Query 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-32/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「Multi-Query」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 Multi-Query 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 3：Reranker

在企业级 Python 开发与大模型应用工程中，**Reranker** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 32 的代码评审中，特别强调以下几点：

1. **为什么学**：Reranker 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 Reranker，Day 39 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 Reranker 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-32/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「Reranker」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 Reranker 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 4：HyDE

在企业级 Python 开发与大模型应用工程中，**HyDE** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 32 的代码评审中，特别强调以下几点：

1. **为什么学**：HyDE 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 HyDE，Day 39 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 HyDE 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-32/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「HyDE」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 HyDE 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方


## 阶段复盘锚点（Phase 3：LangChain RAG 知识库）

今天是 **Phase 3：LangChain RAG 知识库** 的第 **2** 个学习日。请回顾：

- 昨天学了什么？今天如何承接？
- 今天的内容在 70 天路线图中的坐标？
- 如果我是 Tech Lead，会如何 Review 今日代码？

**陈工寄语**：慢即是快。企业里没人关心你一天学了多少个语法点，只关心你写的脚本能不能在服务器上稳定跑 7×24 小时。今天把地基打牢，后面 Agent 编排、RAG 检索才不会塌。

**林悦补充**：产品侧只验收「用户能感知到的价值」。今日交付虽然简单，但「个人信息卡片」本质是后续「用户画像 Agent」的数据采集原型——字段设计请认真思考。

**代码量统计（累计）**：完成今日后，个人仓库累计约 **44800** 行（含注释与测试），全营目标 10 万行。

**明日预告**：请提前阅读 `courseware/day-33/README.md` 开头的旁白，了解上下文。



## 常见问题 FAQ（讲师答疑实录）


**Q1：学习「Query Expansion」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，Query Expansion 用于支撑「高级 RAG（上）」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 Query Expansion 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q2：学习「Multi-Query」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，Multi-Query 用于支撑「高级 RAG（上）」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 Multi-Query 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q3：学习「Reranker」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，Reranker 用于支撑「高级 RAG（上）」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 Reranker 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q4：学习「HyDE」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，HyDE 用于支撑「高级 RAG（上）」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 HyDE 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


## 面试押题（与今日知识点挂钩）

以下题目会出现在 Day 67-69 模拟面试中，建议今日就开始积累答案：

1. **Query Expansion**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
2. **Multi-Query**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
3. **Reranker**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
4. **HyDE**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？

**参考答案思路**：采用 STAR 法则（情境-任务-行动-结果），引用 `courseware/day-32/code/` 中的具体文件名与函数名。

---


## Code Review 检查表（陈工版）

合并 MR 前自查：

- [ ] 所有新增 `.py` 文件顶部有模块说明 docstring
- [ ] 无硬编码密钥（API Key 走环境变量）
- [ ] 函数长度 < 50 行，过长则拆分
- [ ] 异常有明确提示，禁止裸 `except:`
- [ ] 提交信息符合 `feat(day-32): ...`
- [ ] README 或注释说明如何运行
- [ ] 与 Jira Story 验收标准逐条对应

**今日重点审查项**：高级 RAG（上） 相关逻辑是否可读、可测、可扩展至 `platform/nexus_agent/`。

---


## 课后作业

### 作业说明

实现 Multi-Query Retriever：扩展 3 个 query 分别检索后去重合并。

### 提交要求

1. 代码提交到分支 `feature/day-32-homework`
2. GitLab MR 标题：`[Day-32] homework: 课后作业`
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

对每个 query 调用 retriever，用 set 按 page_content 去重。

---


## 附录：Git 提交示例

```bash
git checkout develop
git pull origin develop
git checkout -b feature/day-32-高级-rag（上）
# 完成代码后
git add courseware/day-32/
git commit -m "feat(day-32): 高级 RAG（上）"
git push -u origin feature/day-32-高级-rag（上）
```

---

*课件版本 Day-32-v1.0 | 智链科技培训中心*
