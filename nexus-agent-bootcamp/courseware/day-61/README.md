# Day 61：毕业设计开发：Agent 编排模块

> **阶段**：Phase 6：毕业设计 | **Epic**：NEXUS-E6 | **预计学时**：6-8 小时

## 旁白解读：今日上下文

> 🎬 **模拟站会 09:00** — 智链科技 Nexus 项目组

陈工演示 LangGraph 调试：「Agent 的价值不是聊天，是能自主决定调用什么工具、什么时候该说不。」

**今日在 NexusAgent 主线中的位置**：毕业项目 Agent 引擎

**今日 Jira 看板**：
- `NEXUS-605`

---


## 需求文档（产品林悦下发）

**文档编号**：PRD-NEXUS-D61  
**版本**：v1.0  
**优先级**：P0

### 背景

Phase 6：毕业设计阶段第 61 天教学任务，与 NexusAgent 主线项目对齐。

### User Stories

### NEXUS-605

**描述**：毕业设计开发：Agent 编排模块 相关交付

**验收标准**：
- [ ] 代码可本地运行
- [ ] 通过 `scripts/verify_day.py --day 61`


---


## 今日课表

### 上午 09:00-12:00

- 站会：RAG 检索效果评审
- LangGraph 状态机与 ReAct 模式回顾
- 工具函数设计与 Agent 决策流程
- 检索增强生成（RAG + Agent）架构

### 下午 14:00-17:30

- 实现 agent/graph.py 状态机与工具调用
- 开发 agent/router.py 对话 API
- 联通 RAG 检索工具到 Agent 流程
- 测试 5 个多步推理场景

### 晚自习 19:00-21:00

- 优化 Agent 回答模板与拒答策略
- 记录 Agent 链路日志
- 预习 API 集成与中间件

---


## 课堂笔记

### 核心知识点速查

| 序号 | 知识点 | 代码位置 |
|------|--------|----------|
| 1 | LangGraph 状态机 | 见下午实操 |
| 2 | ReAct 模式 | 见下午实操 |
| 3 | 工具调用 | 见下午实操 |
| 4 | RAG 增强 Agent | 见下午实操 |
| 5 | 拒答策略 | 见下午实操 |

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
flowchart TD
    USER[用户问题] --> AGENT[Agent 状态机]
    AGENT --> DECIDE{需要检索?}
    DECIDE -->|是| TOOL[search_tool]
    TOOL --> RAG[RAG 检索]
    RAG --> SYNTH[合成回答]
    DECIDE -->|否| SYNTH
    SYNTH --> ANSWER[返回用户]
```

---


## 实操代码清单

- `code/graduation_project/nexus_capstone/README.md`
- `code/graduation_project/nexus_capstone/requirements.txt`
- `code/graduation_project/nexus_capstone/app/__init__.py`
- `code/graduation_project/nexus_capstone/app/main.py`
- `code/graduation_project/nexus_capstone/docs/PROJECT_PROPOSAL.md`
- `code/graduation_project/nexus_capstone/docker-compose.dev.yml`
- `code/graduation_project/nexus_capstone/app/auth/__init__.py`
- `code/graduation_project/nexus_capstone/app/auth/models.py`
- `code/graduation_project/nexus_capstone/app/auth/service.py`
- `code/graduation_project/nexus_capstone/app/auth/router.py`
- `code/graduation_project/nexus_capstone/app/rag/__init__.py`
- `code/graduation_project/nexus_capstone/app/rag/ingest.py`
- `code/graduation_project/nexus_capstone/app/rag/retriever.py`
- `code/graduation_project/nexus_capstone/app/rag/router.py`
- `code/graduation_project/nexus_capstone/app/agent/__init__.py`
- `code/graduation_project/nexus_capstone/app/agent/graph.py`
- `code/graduation_project/nexus_capstone/app/agent/router.py`

请按顺序创建并运行。每段代码均可直接复制到对应文件执行。

---

## 实验手册（分时段操作表）

### 实验步骤 1：09:30-10:30 理论

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 61` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-605 | 按附录 Git 示例操作 |


### 实验步骤 2：10:30-12:00 跟敲

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 61` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-605 | 按附录 Git 示例操作 |


### 实验步骤 3：14:00-15:30 实操

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 61` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-605 | 按附录 Git 示例操作 |


### 实验步骤 4：15:30-17:00 联调

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 61` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-605 | 按附录 Git 示例操作 |


### 实验步骤 5：19:00-20:30 作业

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 61` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-605 | 按附录 Git 示例操作 |


### 排错手册（Day 61）

1. **`command not found: python3`** → 安装 Python 3.10+ 或使用 `py -3`（Windows）
2. **`ModuleNotFoundError`** → 确认当前目录、是否激活 venv、`pip install -r requirements.txt`（若当日有）
3. **`SyntaxError: invalid syntax`** → 检查上一行是否缺括号、引号是否中文
4. **`UnicodeDecodeError`** → 文件保存为 UTF-8，终端 `export PYTHONIOENCODING=utf-8`
5. **API 相关（Day12+）** → 检查 `.env` 中 Key，无 Key 时使用课件 MOCK 模式

---


## 逐步跟敲指南（完整源码与解析）

> 以下代码与 `code/` 目录完全一致，可直接复制。每段附行级说明。

### 文件：`code/graduation_project/nexus_capstone/README.md`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/README.md`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 README.md.py`（若为包内模块则按课件说明）

```python
# Nexus Capstone — 毕业设计项目

> 智链科技 NexusAgent 训练营毕业设计脚手架

## 项目简介
基于 70 天所学，构建一个可演示的企业级 AI Agent 应用。

## 技术栈
- FastAPI + SQLAlchemy + Redis
- Chroma 向量检索 + LangGraph Agent 编排
- Docker Compose 一键部署

## 快速启动
```bash
cd graduation_project/nexus_capstone
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 模块进度
- [ ] 用户认证 (Day 59)
- [ ] 知识库 RAG (Day 60)
- [ ] Agent 编排 (Day 61)
- [ ] API 网关 (Day 62)
- [ ] 前端界面 (Day 63)
- [ ] 测试与优化 (Day 64)

```

**解析要点（`graduation_project/nexus_capstone/README.md`）**：

- 共 **26** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/requirements.txt`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/requirements.txt`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 requirements.txt.py`（若为包内模块则按课件说明）

```python
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
redis>=5.0.0
httpx>=0.27.0
chromadb>=0.5.0
pydantic>=2.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
langgraph>=0.2.0

```

**解析要点（`graduation_project/nexus_capstone/requirements.txt`）**：

- 共 **10** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/__init__.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/__init__.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 __init__.py`（若为包内模块则按课件说明）

```python
"""Nexus Capstone 毕业设计应用包"""

```

**解析要点（`graduation_project/nexus_capstone/app/__init__.py`）**：

- 共 **1** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/main.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/main.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 main.py`（若为包内模块则按课件说明）

```python
#!/usr/bin/env python3
"""
Day 58 — 毕业设计入口：FastAPI 应用骨架
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Nexus Capstone",
    description="智链科技训练营毕业设计 — AI Agent 平台",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    """健康检查端点，部署脚本依赖此接口"""
    return {"status": "ok", "service": "nexus-capstone"}


@app.get("/api/v1/info")
def project_info() -> dict:
    """项目元信息，答辩演示用"""
    return {
        "name": "Nexus Capstone",
        "author": "学员姓名",
        "modules": ["auth", "rag", "agent", "api", "frontend"],
        "status": "scaffold",
    }

```

**解析要点（`graduation_project/nexus_capstone/app/main.py`）**：

- 共 **36** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/docs/PROJECT_PROPOSAL.md`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/docs/PROJECT_PROPOSAL.md`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 PROJECT_PROPOSAL.md.py`（若为包内模块则按课件说明）

```python
# 毕业设计选题书

## 1. 项目名称
（填写你的项目名称，如：智链客服智能助手）

## 2. 问题背景
描述要解决的企业痛点（参考智链科技真实场景）

## 3. 核心功能
- 功能 1：
- 功能 2：
- 功能 3：

## 4. 技术方案
| 模块 | 技术选型 | 说明 |
|------|---------|------|
| 后端 | FastAPI | REST API |
| 检索 | Chroma | 向量知识库 |
| Agent | LangGraph | 多步推理编排 |
| 部署 | Docker Compose | 生产级交付 |

## 5. 里程碑
| 天数 | 交付物 |
|------|--------|
| Day 59 | 用户认证模块 |
| Day 60 | RAG 知识库 |
| Day 61 | Agent 编排 |
| Day 62 | API 集成 |
| Day 63 | 前端界面 |
| Day 64 | 测试优化 |
| Day 65 | 答辩 PPT |

```

**解析要点（`graduation_project/nexus_capstone/docs/PROJECT_PROPOSAL.md`）**：

- 共 **31** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/docker-compose.dev.yml`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/docker-compose.dev.yml`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 docker-compose.dev.yml.py`（若为包内模块则按课件说明）

```python
version: "3.9"
services:
  app:
    build: .
    ports: ["8080:8080"]
    environment:
      DATABASE_URL: postgresql://capstone:capstone@db:5432/capstone
      REDIS_URL: redis://redis:6379/0
    depends_on: [db, redis]
  db:
    image: postgres:16-alpine
    environment: {POSTGRES_USER: capstone, POSTGRES_PASSWORD: capstone, POSTGRES_DB: capstone}
  redis:
    image: redis:7-alpine

```

**解析要点（`graduation_project/nexus_capstone/docker-compose.dev.yml`）**：

- 共 **14** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/auth/__init__.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/auth/__init__.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 __init__.py`（若为包内模块则按课件说明）

```python

```

**解析要点（`graduation_project/nexus_capstone/app/auth/__init__.py`）**：

- 共 **0** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/auth/models.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/auth/models.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 models.py`（若为包内模块则按课件说明）

```python
"""Day 59 — 用户数据模型"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

```

**解析要点（`graduation_project/nexus_capstone/app/auth/models.py`）**：

- 共 **15** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/auth/service.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/auth/service.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 service.py`（若为包内模块则按课件说明）

```python
"""Day 59 — 认证服务：注册、登录、JWT"""
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "capstone-dev-secret"  # 生产环境从环境变量读取
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int, expires_hours: int = 24) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=expires_hours),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

```

**解析要点（`graduation_project/nexus_capstone/app/auth/service.py`）**：

- 共 **24** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/auth/router.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/auth/router.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 router.py`（若为包内模块则按课件说明）

```python
"""Day 59 — 认证 API 路由"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/v1/auth", tags=["认证"])

# 内存存储（教学演示，生产用数据库）
_users_db: dict[str, dict] = {}


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(req: RegisterRequest) -> dict:
  if req.username in _users_db:
      raise HTTPException(400, "用户名已存在")
  from app.auth.service import hash_password
  _users_db[req.username] = {"email": req.email, "password": hash_password(req.password)}
  return {"message": "注册成功", "username": req.username}


@router.post("/login")
def login(req: LoginRequest) -> dict:
    user = _users_db.get(req.username)
    if not user:
        raise HTTPException(401, "用户不存在")
    from app.auth.service import verify_password, create_access_token
    if not verify_password(req.password, user["password"]):
        raise HTTPException(401, "密码错误")
    return {"access_token": create_access_token(1), "token_type": "bearer"}

```

**解析要点（`graduation_project/nexus_capstone/app/auth/router.py`）**：

- 共 **39** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/rag/__init__.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/rag/__init__.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 __init__.py`（若为包内模块则按课件说明）

```python

```

**解析要点（`graduation_project/nexus_capstone/app/rag/__init__.py`）**：

- 共 **0** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/rag/ingest.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/rag/ingest.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 ingest.py`（若为包内模块则按课件说明）

```python
"""Day 60 — 文档入库与向量化"""
from pathlib import Path


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """滑动窗口分块，保留上下文重叠"""
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size - overlap
    return chunks


def ingest_document(path: Path, collection_name: str = "capstone_kb") -> int:
    """读取文档并写入 Chroma（Mock 模式返回块数）"""
    text = path.read_text(encoding="utf-8")
    chunks = chunk_text(text)
  # 生产: chroma_client.get_or_create_collection(collection_name).add(...)
    print(f"[ingest] {path.name}: {len(chunks)} 块 -> {collection_name}")
    return len(chunks)

```

**解析要点（`graduation_project/nexus_capstone/app/rag/ingest.py`）**：

- 共 **21** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/rag/retriever.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/rag/retriever.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 retriever.py`（若为包内模块则按课件说明）

```python
"""Day 60 — 混合检索器"""
from dataclasses import dataclass


@dataclass
class RetrievalResult:
    content: str
    score: float
    source: str


class HybridRetriever:
    """向量检索 + 关键词检索融合（教学简化版）"""

    def __init__(self, top_k: int = 5) -> None:
        self.top_k = top_k
        self._docs = [
            RetrievalResult("重置密码请进入管理后台系统设置", 0.92, "faq.md"),
            RetrievalResult("RAG 检索需确保 Chroma 在线", 0.85, "ops.md"),
        ]

    def search(self, query: str) -> list[RetrievalResult]:
        """按关键词匹配模拟混合检索"""
        results = [d for d in self._docs if any(k in d.content for k in query.split())]
        return sorted(results, key=lambda r: r.score, reverse=True)[: self.top_k]

```

**解析要点（`graduation_project/nexus_capstone/app/rag/retriever.py`）**：

- 共 **25** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/rag/router.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/rag/router.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 router.py`（若为包内模块则按课件说明）

```python
"""Day 60 — 知识库 API"""
from fastapi import APIRouter, UploadFile
from app.rag.retriever import HybridRetriever

router = APIRouter(prefix="/api/v1/knowledge", tags=["知识库"])
retriever = HybridRetriever()


@router.post("/upload")
async def upload_document(file: UploadFile) -> dict:
    content = (await file.read()).decode("utf-8")
    from app.rag.ingest import chunk_text
    chunks = chunk_text(content)
    return {"filename": file.filename, "chunks": len(chunks)}


@router.get("/search")
def search_knowledge(q: str) -> dict:
    results = retriever.search(q)
    return {"query": q, "results": [{"content": r.content, "score": r.score, "source": r.source} for r in results]}

```

**解析要点（`graduation_project/nexus_capstone/app/rag/router.py`）**：

- 共 **20** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/agent/__init__.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/agent/__init__.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 __init__.py`（若为包内模块则按课件说明）

```python

```

**解析要点（`graduation_project/nexus_capstone/app/agent/__init__.py`）**：

- 共 **0** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/agent/graph.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/agent/graph.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 graph.py`（若为包内模块则按课件说明）

```python
"""Day 61 — LangGraph Agent 编排"""
from typing import TypedDict


class AgentState(TypedDict):
    """Agent 状态机：记录对话与工具调用上下文"""
    messages: list[dict]
    tool_results: list[str]
    final_answer: str


def search_tool(query: str) -> str:
    """模拟知识库检索工具"""
    from app.rag.retriever import HybridRetriever
    results = HybridRetriever().search(query)
    return "\n".join(r.content for r in results) or "未找到相关内容"


def run_agent(user_query: str) -> str:
    """
    简化版 ReAct Agent 流程：
    1. 判断是否需要检索
    2. 调用工具
    3. 生成最终回答
    """
    state: AgentState = {"messages": [{"role": "user", "content": user_query}], "tool_results": [], "final_answer": ""}

    # 步骤 1: 检索增强
    if any(kw in user_query for kw in ("如何", "怎么", "什么是")):
        tool_output = search_tool(user_query)
        state["tool_results"].append(tool_output)

    # 步骤 2: 合成回答（生产环境调用 LLM）
    context = state["tool_results"][0] if state["tool_results"] else ""
    state["final_answer"] = f"根据知识库：{context}" if context else f"关于「{user_query}」，建议联系人工支持。"
    return state["final_answer"]

```

**解析要点（`graduation_project/nexus_capstone/app/agent/graph.py`）**：

- 共 **36** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/graduation_project/nexus_capstone/app/agent/router.py`

**操作步骤**：
1. 在 `courseware/day-61/code/` 下创建文件 `graduation_project/nexus_capstone/app/agent/router.py`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-61/code && python3 router.py`（若为包内模块则按课件说明）

```python
"""Day 61 — Agent 对话 API"""
from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.graph import run_agent

router = APIRouter(prefix="/api/v1/agent", tags=["Agent"])


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def agent_chat(req: ChatRequest) -> dict:
    answer = run_agent(req.message)
    return {"answer": answer, "agent": "nexus-capstone-v1"}

```

**解析要点（`graduation_project/nexus_capstone/app/agent/router.py`）**：

- 共 **16** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---



### 深度讲解 1：LangGraph 状态机

在企业级 Python 开发与大模型应用工程中，**LangGraph 状态机** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 61 的代码评审中，特别强调以下几点：

1. **为什么学**：LangGraph 状态机 直接服务于后续 NexusAgent 平台的 `NEXUS-E6` 模块。没有扎实的 LangGraph 状态机，Day 68 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 LangGraph 状态机 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-61/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E6 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「LangGraph 状态机」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 LangGraph 状态机 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 2：ReAct 模式

在企业级 Python 开发与大模型应用工程中，**ReAct 模式** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 61 的代码评审中，特别强调以下几点：

1. **为什么学**：ReAct 模式 直接服务于后续 NexusAgent 平台的 `NEXUS-E6` 模块。没有扎实的 ReAct 模式，Day 68 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 ReAct 模式 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-61/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E6 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「ReAct 模式」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 ReAct 模式 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 3：工具调用

在企业级 Python 开发与大模型应用工程中，**工具调用** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 61 的代码评审中，特别强调以下几点：

1. **为什么学**：工具调用 直接服务于后续 NexusAgent 平台的 `NEXUS-E6` 模块。没有扎实的 工具调用，Day 68 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 工具调用 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-61/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E6 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「工具调用」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 工具调用 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 4：RAG 增强 Agent

在企业级 Python 开发与大模型应用工程中，**RAG 增强 Agent** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 61 的代码评审中，特别强调以下几点：

1. **为什么学**：RAG 增强 Agent 直接服务于后续 NexusAgent 平台的 `NEXUS-E6` 模块。没有扎实的 RAG 增强 Agent，Day 68 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 RAG 增强 Agent 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-61/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E6 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「RAG 增强 Agent」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 RAG 增强 Agent 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 5：拒答策略

在企业级 Python 开发与大模型应用工程中，**拒答策略** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 61 的代码评审中，特别强调以下几点：

1. **为什么学**：拒答策略 直接服务于后续 NexusAgent 平台的 `NEXUS-E6` 模块。没有扎实的 拒答策略，Day 68 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 拒答策略 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-61/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E6 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「拒答策略」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 拒答策略 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方


## 阶段复盘锚点（Phase 6：毕业设计）

今天是 **Phase 6：毕业设计** 的第 **1** 个学习日。请回顾：

- 昨天学了什么？今天如何承接？
- 今天的内容在 70 天路线图中的坐标？
- 如果我是 Tech Lead，会如何 Review 今日代码？

**陈工寄语**：慢即是快。企业里没人关心你一天学了多少个语法点，只关心你写的脚本能不能在服务器上稳定跑 7×24 小时。今天把地基打牢，后面 Agent 编排、RAG 检索才不会塌。

**林悦补充**：产品侧只验收「用户能感知到的价值」。今日交付虽然简单，但「个人信息卡片」本质是后续「用户画像 Agent」的数据采集原型——字段设计请认真思考。

**代码量统计（累计）**：完成今日后，个人仓库累计约 **85400** 行（含注释与测试），全营目标 10 万行。

**明日预告**：请提前阅读 `courseware/day-62/README.md` 开头的旁白，了解上下文。



## 常见问题 FAQ（讲师答疑实录）


**Q1：学习「LangGraph 状态机」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E6` 中，LangGraph 状态机 用于支撑「毕业设计开发：Agent 编排模块」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 LangGraph 状态机 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q2：学习「ReAct 模式」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E6` 中，ReAct 模式 用于支撑「毕业设计开发：Agent 编排模块」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 ReAct 模式 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q3：学习「工具调用」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E6` 中，工具调用 用于支撑「毕业设计开发：Agent 编排模块」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 工具调用 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q4：学习「RAG 增强 Agent」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E6` 中，RAG 增强 Agent 用于支撑「毕业设计开发：Agent 编排模块」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 RAG 增强 Agent 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q5：学习「拒答策略」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E6` 中，拒答策略 用于支撑「毕业设计开发：Agent 编排模块」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 拒答策略 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


## 面试押题（与今日知识点挂钩）

以下题目会出现在 Day 67-69 模拟面试中，建议今日就开始积累答案：

1. **LangGraph 状态机**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
2. **ReAct 模式**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
3. **工具调用**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
4. **RAG 增强 Agent**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
5. **拒答策略**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？

**参考答案思路**：采用 STAR 法则（情境-任务-行动-结果），引用 `courseware/day-61/code/` 中的具体文件名与函数名。

---


## Code Review 检查表（陈工版）

合并 MR 前自查：

- [ ] 所有新增 `.py` 文件顶部有模块说明 docstring
- [ ] 无硬编码密钥（API Key 走环境变量）
- [ ] 函数长度 < 50 行，过长则拆分
- [ ] 异常有明确提示，禁止裸 `except:`
- [ ] 提交信息符合 `feat(day-61): ...`
- [ ] README 或注释说明如何运行
- [ ] 与 Jira Story 验收标准逐条对应

**今日重点审查项**：毕业设计开发：Agent 编排模块 相关逻辑是否可读、可测、可扩展至 `platform/nexus_agent/`。

---


## 课后作业

### 作业说明

实现 Agent 对话 API，至少支持检索增强回答。测试 5 个场景：3 个知识库可回答 + 2 个应拒答/转人工。

### 提交要求

1. 代码提交到分支 `feature/day-61-homework`
2. GitLab MR 标题：`[Day-61] homework: 课后作业`
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

run_agent 先判断是否需要检索，调用 search_tool，再合成回答。超范围问题返回「建议联系人工支持」。

---


## 附录：Git 提交示例

```bash
git checkout develop
git pull origin develop
git checkout -b feature/day-61-毕业设计开发：age
# 完成代码后
git add courseware/day-61/
git commit -m "feat(day-61): 毕业设计开发：Agent 编排模块"
git push -u origin feature/day-61-毕业设计开发：age
```

---

*课件版本 Day-61-v1.0 | 智链科技培训中心*
