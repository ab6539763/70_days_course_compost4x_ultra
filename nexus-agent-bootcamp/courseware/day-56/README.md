# Day 56：Docker Compose 生产级部署

> **阶段**：Phase 5：微调与部署 | **Epic**：NEXUS-E5 | **预计学时**：6-8 小时

## 旁白解读：今日上下文

> 🎬 **模拟站会 09:00** — 智链科技 Nexus 项目组

运维老王加入站会：「生产环境不允许裸跑 Python 进程。今天交付的 docker-compose 要能在一台新机器上 10 分钟拉起全栈。」

**今日在 NexusAgent 主线中的位置**：NexusAgent v0.5 生产部署架构落地

**今日 Jira 看板**：
- `NEXUS-511`
- `NEXUS-512`
- `NEXUS-513`

---


## 需求文档（产品林悦下发）

**文档编号**：PRD-NEXUS-D56  
**版本**：v1.0  
**优先级**：P0

### 背景

Phase 5：微调与部署阶段第 56 天教学任务，与 NexusAgent 主线项目对齐。

### User Stories

### NEXUS-511

**描述**：Docker Compose 生产级部署 相关交付

**验收标准**：
- [ ] 代码可本地运行
- [ ] 通过 `scripts/verify_day.py --day 56`

### NEXUS-512

**描述**：Docker Compose 生产级部署 相关交付

**验收标准**：
- [ ] 代码可本地运行
- [ ] 通过 `scripts/verify_day.py --day 56`

### NEXUS-513

**描述**：Docker Compose 生产级部署 相关交付

**验收标准**：
- [ ] 代码可本地运行
- [ ] 通过 `scripts/verify_day.py --day 56`


---


## 今日课表

### 上午 09:00-12:00

- 站会：确认 vLLM 服务稳定运行
- Docker 多阶段构建与镜像优化
- docker-compose.yml 服务编排讲解
- Nginx 反向代理与 SSE 流式配置

### 下午 14:00-17:30

- 编写并调试 docker-compose.yml 全栈编排
- 构建 Dockerfile.api 应用镜像
- 运行 deploy.sh 一键部署
- health_check.sh 全链路验证 + rollback.sh 演练

### 晚自习 19:00-21:00

- 完整部署截图：docker compose ps + 健康检查
- 编写部署文档（环境变量、端口、依赖）
- 预习安全合规要求

---


## 课堂笔记

### 核心知识点速查

| 序号 | 知识点 | 代码位置 |
|------|--------|----------|
| 1 | Docker Compose 编排 | 见下午实操 |
| 2 | 多服务依赖管理 | 见下午实操 |
| 3 | Nginx 反向代理 | 见下午实操 |
| 4 | 健康检查 | 见下午实操 |
| 5 | 一键部署脚本 | 见下午实操 |

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
flowchart TB
    NGINX[Nginx :80] --> API[FastAPI :8080]
    API --> PG[(PostgreSQL)]
    API --> REDIS[(Redis)]
    API --> CHROMA[(Chroma)]
    API --> VLLM[vLLM :8000]
    API --> MINIO[(MinIO)]
```

---


## 实操代码清单

- `code/deploy/docker-compose.yml`
- `code/deploy/Dockerfile.api`
- `code/deploy/nginx/nginx.conf`
- `code/deploy/scripts/deploy.sh`
- `code/deploy/scripts/rollback.sh`
- `code/deploy/scripts/health_check.sh`
- `code/deploy/requirements.txt`

请按顺序创建并运行。每段代码均可直接复制到对应文件执行。

---

## 实验手册（分时段操作表）

### 实验步骤 1：09:30-10:30 理论

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 56` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-511 | 按附录 Git 示例操作 |


### 实验步骤 2：10:30-12:00 跟敲

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 56` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-511 | 按附录 Git 示例操作 |


### 实验步骤 3：14:00-15:30 实操

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 56` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-511 | 按附录 Git 示例操作 |


### 实验步骤 4：15:30-17:00 联调

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 56` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-511 | 按附录 Git 示例操作 |


### 实验步骤 5：19:00-20:30 作业

| 时间 | 动作 | 预期结果 | 失败处理 |
|------|------|----------|----------|
| +0min | 打开课件本节 | 看到需求与验收标准 | 检查是否拉取最新 `develop` 分支 |
| +10min | 创建/打开当日 `code/` 文件 | 文件路径与清单一致 | 对照「实操代码清单」 |
| +30min | 粘贴并运行第一个脚本 | 终端有正常输出无 Traceback | 见下方「排错手册」 |
| +60min | 完成全部文件并自测 | `python3` 运行通过 | 使用 `scripts/verify_day.py --day 56` |
| +90min | 提交 Git 并建 MR | MR 关联 Jira NEXUS-511 | 按附录 Git 示例操作 |


### 排错手册（Day 56）

1. **`command not found: python3`** → 安装 Python 3.10+ 或使用 `py -3`（Windows）
2. **`ModuleNotFoundError`** → 确认当前目录、是否激活 venv、`pip install -r requirements.txt`（若当日有）
3. **`SyntaxError: invalid syntax`** → 检查上一行是否缺括号、引号是否中文
4. **`UnicodeDecodeError`** → 文件保存为 UTF-8，终端 `export PYTHONIOENCODING=utf-8`
5. **API 相关（Day12+）** → 检查 `.env` 中 Key，无 Key 时使用课件 MOCK 模式

---


## 逐步跟敲指南（完整源码与解析）

> 以下代码与 `code/` 目录完全一致，可直接复制。每段附行级说明。

### 文件：`code/deploy/docker-compose.yml`

**操作步骤**：
1. 在 `courseware/day-56/code/` 下创建文件 `deploy/docker-compose.yml`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-56/code && python3 docker-compose.yml.py`（若为包内模块则按课件说明）

```python
version: "3.9"
services:
  nginx:
    image: nginx:1.25-alpine
    ports: ["80:80"]
    volumes: ["./nginx/nginx.conf:/etc/nginx/nginx.conf:ro"]
    depends_on: [api]
    networks: [nexus-net]
  api:
    build: {context: ../.., dockerfile: deploy/Dockerfile.api}
    environment:
      DATABASE_URL: postgresql://nexus:nexus_secret@postgres:5432/nexus_db
      REDIS_URL: redis://redis:6379/0
      LLM_BASE_URL: http://vllm:8000/v1
    depends_on: {postgres: {condition: service_healthy}}
    networks: [nexus-net]
  vllm:
    image: vllm/vllm-openai:latest
    command: "--model /models/nexus-qwen-merged --host 0.0.0.0 --port 8000"
    volumes: ["./models:/models:ro"]
    deploy:
      resources: {reservations: {devices: [{driver: nvidia, count: 1, capabilities: [gpu]}]}}
    networks: [nexus-net]
  chroma:
    image: chromadb/chroma:0.5.5
    volumes: [chroma_data:/chroma/chroma]
    networks: [nexus-net]
  postgres:
    image: postgres:16-alpine
    environment: {POSTGRES_USER: nexus, POSTGRES_PASSWORD: nexus_secret, POSTGRES_DB: nexus_db}
    healthcheck: {test: ["CMD-SHELL", "pg_isready -U nexus"], interval: 5s, retries: 5}
    volumes: [postgres_data:/var/lib/postgresql/data]
    networks: [nexus-net]
  redis:
    image: redis:7-alpine
    networks: [nexus-net]
volumes: {postgres_data: {}, chroma_data: {}}
networks: {nexus-net: {driver: bridge}}

```

**解析要点（`deploy/docker-compose.yml`）**：

- 共 **38** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/deploy/Dockerfile.api`

**操作步骤**：
1. 在 `courseware/day-56/code/` 下创建文件 `deploy/Dockerfile.api`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-56/code && python3 Dockerfile.api.py`（若为包内模块则按课件说明）

```python
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY platform/ ./platform/
CMD ["uvicorn", "platform.nexus_agent.main:app", "--host", "0.0.0.0", "--port", "8080"]

```

**解析要点（`deploy/Dockerfile.api`）**：

- 共 **6** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/deploy/nginx/nginx.conf`

**操作步骤**：
1. 在 `courseware/day-56/code/` 下创建文件 `deploy/nginx/nginx.conf`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-56/code && python3 nginx.conf.py`（若为包内模块则按课件说明）

```python
worker_processes auto;
events { worker_connections 1024; }
http {
  upstream nexus_api { server api:8080; }
  server {
    listen 80;
    location /api/ { proxy_pass http://nexus_api/; proxy_buffering off; }
    location /health { proxy_pass http://nexus_api/health; }
  }
}

```

**解析要点（`deploy/nginx/nginx.conf`）**：

- 共 **10** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/deploy/scripts/deploy.sh`

**操作步骤**：
1. 在 `courseware/day-56/code/` 下创建文件 `deploy/scripts/deploy.sh`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-56/code && python3 deploy.sh.py`（若为包内模块则按课件说明）

```python
#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo "=== NexusAgent 部署 ==="
docker compose build api
docker compose up -d
for i in $(seq 1 30); do
  curl -sf http://localhost/health && echo "✅ 部署成功" && exit 0
  sleep 2
done
echo "❌ 健康检查超时"; exit 1

```

**解析要点（`deploy/scripts/deploy.sh`）**：

- 共 **11** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/deploy/scripts/rollback.sh`

**操作步骤**：
1. 在 `courseware/day-56/code/` 下创建文件 `deploy/scripts/rollback.sh`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-56/code && python3 rollback.sh.py`（若为包内模块则按课件说明）

```python
#!/bin/bash
cd "$(dirname "$0")/.."
docker compose down
echo "回滚完成"

```

**解析要点（`deploy/scripts/rollback.sh`）**：

- 共 **4** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/deploy/scripts/health_check.sh`

**操作步骤**：
1. 在 `courseware/day-56/code/` 下创建文件 `deploy/scripts/health_check.sh`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-56/code && python3 health_check.sh.py`（若为包内模块则按课件说明）

```python
#!/bin/bash
curl -sf http://localhost/health && echo "✅ API" || echo "❌ API"

```

**解析要点（`deploy/scripts/health_check.sh`）**：

- 共 **2** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---

### 文件：`code/deploy/requirements.txt`

**操作步骤**：
1. 在 `courseware/day-56/code/` 下创建文件 `deploy/requirements.txt`
2. 完整粘贴下方代码
3. 在终端执行：`cd courseware/day-56/code && python3 requirements.txt.py`（若为包内模块则按课件说明）

```python
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
httpx>=0.27.0

```

**解析要点（`deploy/requirements.txt`）**：

- 共 **3** 行，请逐行阅读注释中的中文说明

- 运行前确认 Python 版本 ≥ 3.10：`python3 --version`

- 若报错，先检查缩进是否为 4 空格，勿混用 Tab

- 企业 Review 清单：命名是否清晰、是否有异常处理、是否可复用

---



### 深度讲解 1：Docker Compose 编排

在企业级 Python 开发与大模型应用工程中，**Docker Compose 编排** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 56 的代码评审中，特别强调以下几点：

1. **为什么学**：Docker Compose 编排 直接服务于后续 NexusAgent 平台的 `NEXUS-E5` 模块。没有扎实的 Docker Compose 编排，Day 63 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 Docker Compose 编排 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-56/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E5 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「Docker Compose 编排」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 Docker Compose 编排 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 2：多服务依赖管理

在企业级 Python 开发与大模型应用工程中，**多服务依赖管理** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 56 的代码评审中，特别强调以下几点：

1. **为什么学**：多服务依赖管理 直接服务于后续 NexusAgent 平台的 `NEXUS-E5` 模块。没有扎实的 多服务依赖管理，Day 63 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 多服务依赖管理 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-56/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E5 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「多服务依赖管理」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 多服务依赖管理 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 3：Nginx 反向代理

在企业级 Python 开发与大模型应用工程中，**Nginx 反向代理** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 56 的代码评审中，特别强调以下几点：

1. **为什么学**：Nginx 反向代理 直接服务于后续 NexusAgent 平台的 `NEXUS-E5` 模块。没有扎实的 Nginx 反向代理，Day 63 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 Nginx 反向代理 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-56/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E5 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「Nginx 反向代理」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 Nginx 反向代理 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 4：健康检查

在企业级 Python 开发与大模型应用工程中，**健康检查** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 56 的代码评审中，特别强调以下几点：

1. **为什么学**：健康检查 直接服务于后续 NexusAgent 平台的 `NEXUS-E5` 模块。没有扎实的 健康检查，Day 63 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 健康检查 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-56/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E5 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「健康检查」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 健康检查 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方



### 深度讲解 5：一键部署脚本

在企业级 Python 开发与大模型应用工程中，**一键部署脚本** 是学员必须牢固掌握的基本功。智链科技 Nexus 项目组在 Day 56 的代码评审中，特别强调以下几点：

1. **为什么学**：一键部署脚本 直接服务于后续 NexusAgent 平台的 `NEXUS-E5` 模块。没有扎实的 一键部署脚本，Day 63 之后调用 API、解析 JSON、编写 Agent 工具函数时会出现大量低级错误。

2. **常见坑**：
   - 忽略输入类型校验，导致运行时 `TypeError`
   - 编码问题（Windows 默认 GBK vs UTF-8）
   - 复制粘贴时缩进错乱（Python 对缩进敏感）

3. **企业实践**：在 SmartLink 的 GitLab 仓库中，所有与 一键部署脚本 相关的代码必须经过 Ruff 静态检查；变量命名使用 `snake_case`，常量使用 `UPPER_SNAKE_CASE`。

4. **与主线项目的关系**：今日代码位于 `courseware/day-56/code/`，部分模块将逐步合并到 `platform/nexus_agent/`。请养成「每日代码皆可运行、皆可测试」的习惯。

5. **扩展阅读建议**：完成今日作业后，可阅读 `docs/project-master-plan.md` 中关于 NEXUS-E5 的章节，建立全局视角。

**课堂互动题**：请用 3 句话向非技术同事解释「一键部署脚本」是什么。写在作业 MR 的评论里，讲师会抽查点评。

**实操检查清单**：
- [ ] 能不看课件复述 一键部署脚本 的定义
- [ ] 能独立写出相关代码并运行
- [ ] 能向同学讲解一处容易写错的地方


## 阶段复盘锚点（Phase 5：微调与部署）

今天是 **Phase 5：微调与部署** 的第 **6** 个学习日。请回顾：

- 昨天学了什么？今天如何承接？
- 今天的内容在 70 天路线图中的坐标？
- 如果我是 Tech Lead，会如何 Review 今日代码？

**陈工寄语**：慢即是快。企业里没人关心你一天学了多少个语法点，只关心你写的脚本能不能在服务器上稳定跑 7×24 小时。今天把地基打牢，后面 Agent 编排、RAG 检索才不会塌。

**林悦补充**：产品侧只验收「用户能感知到的价值」。今日交付虽然简单，但「个人信息卡片」本质是后续「用户画像 Agent」的数据采集原型——字段设计请认真思考。

**代码量统计（累计）**：完成今日后，个人仓库累计约 **78400** 行（含注释与测试），全营目标 10 万行。

**明日预告**：请提前阅读 `courseware/day-57/README.md` 开头的旁白，了解上下文。



## 常见问题 FAQ（讲师答疑实录）


**Q1：学习「Docker Compose 编排」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E5` 中，Docker Compose 编排 用于支撑「Docker Compose 生产级部署」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 Docker Compose 编排 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q2：学习「多服务依赖管理」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E5` 中，多服务依赖管理 用于支撑「Docker Compose 生产级部署」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 多服务依赖管理 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q3：学习「Nginx 反向代理」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E5` 中，Nginx 反向代理 用于支撑「Docker Compose 生产级部署」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 Nginx 反向代理 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q4：学习「健康检查」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E5` 中，健康检查 用于支撑「Docker Compose 生产级部署」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 健康检查 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


**Q5：学习「一键部署脚本」时最常问的问题是什么？**

A：学员常问「这在大模型开发里到底用在哪里」。直接回答：在 NexusAgent 的 `NEXUS-E5` 中，一键部署脚本 用于支撑「Docker Compose 生产级部署」这一交付。建议你打开 `platform/` 对照看未来模块如何引用今日写法。另一个常见问题是「要不要背语法」——不需要背，但要能写出可运行代码，并能在报错时读懂 Traceback。

**追问**：如果线上报错与 一键部署脚本 相关，如何排查？  
**答**：① 复现 ② 最小化输入 ③ 打印中间变量 ④ 查 GitLab 历史 diff ⑤ 在 Jira 建 Bug 单附上日志。


## 面试押题（与今日知识点挂钩）

以下题目会出现在 Day 67-69 模拟面试中，建议今日就开始积累答案：

1. **Docker Compose 编排**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
2. **多服务依赖管理**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
3. **Nginx 反向代理**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
4. **健康检查**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？
5. **一键部署脚本**：请结合 NexusAgent 项目举例说明你在哪一天、哪段代码里用到了它？

**参考答案思路**：采用 STAR 法则（情境-任务-行动-结果），引用 `courseware/day-56/code/` 中的具体文件名与函数名。

---


## Code Review 检查表（陈工版）

合并 MR 前自查：

- [ ] 所有新增 `.py` 文件顶部有模块说明 docstring
- [ ] 无硬编码密钥（API Key 走环境变量）
- [ ] 函数长度 < 50 行，过长则拆分
- [ ] 异常有明确提示，禁止裸 `except:`
- [ ] 提交信息符合 `feat(day-56): ...`
- [ ] README 或注释说明如何运行
- [ ] 与 Jira Story 验收标准逐条对应

**今日重点审查项**：Docker Compose 生产级部署 相关逻辑是否可读、可测、可扩展至 `platform/nexus_agent/`。

---


## 课后作业

### 作业说明

使用 deploy/docker-compose.yml 完成全栈部署（API + vLLM + Postgres + Redis + Chroma + Nginx）。提交 deploy.sh 执行日志和健康检查截图。

### 提交要求

1. 代码提交到分支 `feature/day-56-homework`
2. GitLab MR 标题：`[Day-56] homework: 课后作业`
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

模型文件放 deploy/models/nexus-qwen-merged/。无 GPU 可注释 vLLM 服务，设 LLM_BASE_URL 为外部 API。健康检查 curl http://localhost/health 返回 200。

---


## 附录：Git 提交示例

```bash
git checkout develop
git pull origin develop
git checkout -b feature/day-56-docker-com
# 完成代码后
git add courseware/day-56/
git commit -m "feat(day-56): Docker Compose 生产级部署"
git push -u origin feature/day-56-docker-com
```

---

*课件版本 Day-56-v1.0 | 智链科技培训中心*
