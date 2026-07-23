# Day 27：Memory 对话记忆

> **阶段**：Phase 3：LangChain RAG 知识库 | **Epic**：NEXUS-E3 | **预计学时**：6-8 小时

## 旁白解读：今日上下文

> 🎬 **模拟站会 09:00** — 智链科技 Nexus 项目组

**林悦**：客服场景必须记住上文。**陈工**：生产用 Redis，今天先用内存字典理解模型。

**今日在 NexusAgent 主线中的位置**：对齐 NexusAgent Redis 会话模块设计

**今日 Jira 看板**：
- `NEXUS-271`
- `NEXUS-272`

---


## 需求文档（产品林悦下发）

**文档编号**：PRD-NEXUS-D27  
**版本**：v1.0  
**优先级**：P0

### 背景

Phase 3：LangChain RAG 知识库阶段第 27 天教学任务，与 NexusAgent 主线项目对齐。

### User Stories

### NEXUS-271

**描述**：Memory 对话记忆 相关交付

**验收标准**：
- [ ] 代码可本地运行
- [ ] 通过 `scripts/verify_day.py --day 27`

### NEXUS-272

**描述**：Memory 对话记忆 相关交付

**验收标准**：
- [ ] 代码可本地运行
- [ ] 通过 `scripts/verify_day.py --day 27`


---


## 今日课表

### 上午 09:00-12:00

- 09:00 ConversationBufferMemory 原理
- 10:00 ChatMessageHistory 持久化
- 11:00 多轮对话链

### 下午 14:00-17:30

- 14:00 实现带记忆的客服链
- 16:00 Redis 会话存储预习
- 17:00 记忆窗口截断策略

### 晚自习 19:00-21:00

- 19:00 作业：限制记忆 10 轮
- 20:00 预习文档分割

---


## 课堂笔记

### 核心知识点速查

| 序号 | 知识点 | 代码位置 |
|------|--------|----------|
| 1 | ConversationBufferMemory | 见下午实操 |
| 2 | 滑动窗口 | 见下午实操 |
| 3 | 会话持久化 | 见下午实操 |
| 4 | token 控制 | 见下午实操 |

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
flowchart LR\n  USER --> CHAIN --> MEMORY --> LLM\n  MEMORY --> HISTORY[(消息历史)]
```

---


## 实操代码清单

- `code/conversation_buffer.py`
- `code/chat_session.py`
- `code/memory_window.py`

请按顺序创建并运行。每段代码均可直接复制到对应文件执行。

---

## 实验手册（分时段操作表）

### 实验步骤 1：09:30-10:30 理论

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 27` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-271 | 按附录 Git 示例操作 |


### 实验步骤 2：10:30-12:00 跟敲

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 27` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-271 | 按附录 Git 示例操作 |


### 实验步骤 3：14:00-15:30 实操

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 27` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-271 | 按附录 Git 示例操作 |


### 实验步骤 4：15:30-17:00 联调

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 27` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-271 | 按附录 Git 示例操作 |


### 实验步骤 5：19:00-20:30 作业

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 27` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-271 | 按附录 Git 示例操作 |


### 排错手册（Day 27）

1. **`command not found: python3`** → 安装 Python 3.10+ 或使用 `py -3`（Windows）
2. **`ModuleNotFoundError`** → 确认当前目录、是否激活 venv、`pip install -r requirements.txt`（若当日有）
3. **`SyntaxError: invalid syntax`** → 检查上一行是否缺括号、引号是否中文
4. **`UnicodeDecodeError`** → 文件保存为 UTF-8，终端 `export PYTHONIOENCODING=utf-8`
5. **API 相关（Day12+）** → 检查 `.env` 中 Key，无 Key 时使用课件 MOCK 模式

---


## 逐步跟敲指南（完整源码与解析）

> 以下代码与 `code/` 目录完全一致，可直接复制。每段附行级说明。

### 文件：`code/conversation_buffer.py`

**操作步骤**：
1. 在 `courseware/day-27/code/` 下创建文件 `conversation_buffer.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-27/code && python3 conversation_buffer.py`（若为包内模块则按课件说明）

```python
#!/usr/bin/env python3
"""Day 27: ConversationBufferMemory 多轮对话"""
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

def build_chain() -> ConversationChain:
  # 缓冲全部历史消息
  memory = ConversationBufferMemory()
  llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
  )
  return ConversationChain(llm=llm, memory=memory, verbose=True)

if __name__ == "__main__":
  chain = build_chain()
  print(chain.predict(input="我叫小明，在智链科技实习。"))
  print(chain.predict(input="我叫什么？在哪实习？"))

```

**解析要点（`conversation_buffer.py`）**：

- 共 **21** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/chat_session.py`

**操作步骤**：
1. 在 `courseware/day-27/code/` 下创建文件 `chat_session.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-27/code && python3 chat_session.py`（若为包内模块则按课件说明）

```python
#!/usr/bin/env python3
"""Day 27: 会话 ID 与内存字典模拟 Redis"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ChatSession:
  session_id: str
  messages: list[dict[str, str]] = field(default_factory=list)

  def append(self, role: str, content: str) -> None:
    self.messages.append({"role": role, "content": content})

  def context_text(self, max_turns: int = 10) -> str:
    # 只保留最近 max_turns 轮，防止 token 爆炸
    recent = self.messages[-(max_turns * 2):]
    return "\n".join(f"{m['role']}: {m['content']}" for m in recent)

SESSION_STORE: dict[str, ChatSession] = {}

def get_session(sid: str) -> ChatSession:
  if sid not in SESSION_STORE:
    SESSION_STORE[sid] = ChatSession(session_id=sid)
  return SESSION_STORE[sid]

if __name__ == "__main__":
  s = get_session("user-001")
  s.append("user", "Nexus 支持私有化吗？")
  s.append("assistant", "支持 Docker 私有化部署。")
  print(s.context_text())

```

**解析要点（`chat_session.py`）**：

- 共 **30** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/memory_window.py`

**操作步骤**：
1. 在 `courseware/day-27/code/` 下创建文件 `memory_window.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-27/code && python3 memory_window.py`（若为包内模块则按课件说明）

```python
#!/usr/bin/env python3
"""Day 27: ConversationBufferWindowMemory 滑动窗口"""
import os
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

memory = ConversationBufferWindowMemory(k=2)  # 仅保留最近 2 轮
llm = ChatOpenAI(
  model="deepseek-chat",
  api_key=os.getenv("DEEPSEEK_API_KEY", "mock"),
  base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
chain = ConversationChain(llm=llm, memory=memory)

if __name__ == "__main__":
  for q in ["A", "B", "C", "你还记得 A 吗？"]:
    print("Q:", q)
    print("A:", chain.predict(input=q)[:80])

```

**解析要点（`memory_window.py`）**：

- 共 **19** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---



### 深度讲解 1：ConversationBufferMemory

在企业级 Python 开发与大模型应用工程中，**ConversationBufferMemory** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 27 的代码评审中，特别强调以下几点：

1. **为什么学**：ConversationBufferMemory 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 ConversationBufferMemory，Day 34 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 ConversationBufferMemory 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-27/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「ConversationBufferMemory」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 ConversationBufferMemory 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 2：滑动窗口

在企业级 Python 开发与大模型应用工程中，**滑动窗口** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 27 的代码评审中，特别强调以下几点：

1. **为什么学**：滑动窗口 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 滑动窗口，Day 34 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 滑动窗口 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-27/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「滑动窗口」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 滑动窗口 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 3：会话持久化

在企业级 Python 开发与大模型应用工程中，**会话持久化** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 27 的代码评审中，特别强调以下几点：

1. **为什么学**：会话持久化 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 会话持久化，Day 34 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 会话持久化 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-27/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「会话持久化」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 会话持久化 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 4：token 控制

在企业级 Python 开发与大模型应用工程中，**token 控制** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 27 的代码评审中，特别强调以下几点：

1. **为什么学**：token 控制 直接服务于后续 NexusAgent 平台的 `NEXUS-E3` 模块。没有扎实的 token 控制，Day 34 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 token 控制 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-27/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E3 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「token 控制」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 token 控制 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方


## 阶段复盘锚点（Phase 3：LangChain RAG 知识库）

今天是 **Phase 3：LangChain RAG 知识库** 的第 **7** 个学习日。请回顾：

- 昨天学了什么？今天如何承接？
- 今天的内容在 70 天路线图中的坐标？
- 如果我是 Tech Lead，会如何 Review 今日代码？

**陈工寄语**：慢即是快。企业里没人关心你一天学了多少个语法点，只关心你写的脚本能不能在服务器上稳定跑 7×24 小时。今天把地基打牢，后面 Agent 编排、RAG 检索才不会塌。

**林悦补充**：产品侧只验收「用户能感知到的价值」。今日交付虽然简单，但「个人信息卡片」本质是后续「用户画像 Agent」的数据采集原型——字段设计请认真思考。

**代码量统计（累计）**：完成今日后，个人仓库累计约 **37800** 行（含注释与测试），全营目标 10 万行。

**明日预告**：请提前阅读 `courseware/day-28/README.md` 开头的旁白，了解上下文。



## 常见问题 FAQ（讲师答疑实录）


**Q1：学习「ConversationBufferMemory」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，ConversationBufferMemory 用于支撑「Memory 对话记忆」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 ConversationBufferMemory 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q2：学习「滑动窗口」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，滑动窗口 用于支撑「Memory 对话记忆」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 滑动窗口 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q3：学习「会话持久化」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，会话持久化 用于支撑「Memory 对话记忆」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 会话持久化 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q4：学习「token 控制」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E3` 中，token 控制 用于支撑「Memory 对话记忆」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 token 控制 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


## 面试押题（与今日知识点挂钩）

以下题目会出现在 Day 67-69 模拟面试中，建议今日就开始积累答案：

1. **ConversationBufferMemory**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
2. **滑动窗口**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
3. **会话持久化**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
4. **token 控制**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？

**参考答案思路**：采用 STAR 法则（情境-任务-行动-结果），引用 `courseware/day-27/code/` 中的具体文件名与函数名。

---


## Code Review 检查表（陈工版）

合并 MR 前自查：

- [ ] 所有新增 `.py` 文件顶部有模块说明 docstring
- [ ] 无硬编码密钥（API Key 走环境变量）
- [ ] 函数长度 < 50 行，过长则拆分
- [ ] 异常有明确提示，禁止裸 `except:`
- [ ] 提交信息符合 `feat(day-27): ...`
- [ ] README 或注释说明如何运行
- [ ] 与 Jira Story 验收标准逐条对应

**今日重点审查项**：Memory 对话记忆 相关逻辑是否可读、可测、可扩展至 `platform/nexus_agent/`。

---


## 课后作业

### 作业说明

扩展 chat_session.py：将会话序列化到 data/sessions/{id}.json，重启可恢复。

### 提交要求

1. 代码提交到分支 `feature/day-27-homework`
2. GitLab MR 标题：`[Day-27] homework: 课后作业`
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

json.dump(messages) 写入，启动时 json.load 恢复。

---


## 附录：Git 提交示例

```bash
git checkout develop
git pull origin develop
git checkout -b feature/day-27-memory-对话记
# 完成代码后
git add courseware/day-27/
git commit -m "feat(day-27): Memory 对话记忆"
git push -u origin feature/day-27-memory-对话记
```

---

*课件版本 Day-27-v1.0 | 智链科技培训中心*
