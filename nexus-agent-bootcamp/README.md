# NexusAgent 企业级智能体平台 — 70天零基础大模型应用开发训练营

> **智链科技（SmartLink Tech）内部培训 + 开源教学版**  
> 用真实企业业务需求驱动，从 0 到 1 搭建可上线的 Agent 企业级平台

## 课程定位

| 项目 | 说明 |
|------|------|
| 培训周期 | 70 天（10 周），每天 6-8 小时 |
| 目标学员 | 零编程基础或少量基础的转行者、在校生、产品经理 |
| 培养目标 | 独立开发 RAG、Agent、微调小模型并部署上线 |
| 主线项目 | **NexusAgent Platform**（灵犀智能体协作平台） |
| 协作模拟 | Jira（需求/缺陷）+ GitLab（代码/CI/CD） |
| 累计代码量 | 约 10 万行（含平台代码、测试、脚本、配置） |

## 目录结构

```
nexus-agent-bootcamp/
├── README.md                    # 本文件
├── docs/                        # 全局文档
│   ├── curriculum-overview.md   # 70天课表总览
│   ├── project-master-plan.md   # 平台从0到1主计划
│   ├── team-roles.md            # 模拟团队角色与分工
│   ├── jira-gitlab-workflow.md  # 协作流程规范
│   └── architecture-evolution.md # 架构演进路线图
├── platform/                    # 主线项目代码（逐日迭代）
│   ├── nexus_agent/             # 核心 Python 包
│   ├── frontend/                # Web 前端（Day 22+）
│   ├── docker/                  # 容器化（Day 56+）
│   └── tests/                   # 测试用例
├── courseware/                  # 每日课件
│   ├── day-01/                  # 第1天
│   │   ├── README.md            # 主课件（≥20000字）
│   │   ├── code/                # 当日可运行代码
│   │   ├── homework/            # 作业与参考答案
│   │   ├── assets/              # 流程图、架构图
│   │   └── jira/                # 当日关联 Jira 工单
│   ├── day-02/
│   └── ... day-70/
└── scripts/                     # 工具脚本
    └── verify_day.py            # 验证当日代码可运行
```

## 主线项目：NexusAgent Platform 演进路线

| 阶段 | 天数 | 交付物 |
|------|------|--------|
| 第一阶段 | Day 1-14 | 命令行多轮对话 AI 助手（项目一） |
| 第二阶段 | Day 15-24 | Web 版 Chat + FastAPI 后端 |
| 第三阶段 | Day 25-38 | 企业知识库 RAG 问答系统（项目二） |
| 第四阶段 | Day 39-50 | 多 Agent 智能办公助手（项目三） |
| 第五阶段 | Day 51-60 | 微调模型 + Docker 部署上线 |
| 第六阶段 | Day 58-70 | 毕业设计 + 就业冲刺 |

## 快速开始（学员）

```bash
# 1. 克隆仓库
git clone <your-gitlab-url>/nexus-agent-bootcamp.git
cd nexus-agent-bootcamp

# 2. 进入第1天课件
cd courseware/day-01

# 3. 按 README.md 逐步操作
python3 --version  # 需要 Python 3.10+
```

## 每日学习节奏

- **09:00-12:00** 授课 + 需求评审模拟
- **14:00-17:30** 编码实操（跟课件逐步粘贴）
- **19:00-21:00** 自习答疑 + 作业

## 许可证

MIT License — 教学用途开源
