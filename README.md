# NexusAgent 70天零基础大模型应用开发训练营

本仓库包含完整的 **70 天企业级培训课程**，以 **NexusAgent 智能体协作平台** 为主线项目，模拟智链科技从 0 到 1 的研发全流程。

## 快速入口

👉 **[进入训练营 `nexus-agent-bootcamp/`](./nexus-agent-bootcamp/)**

## 内容概览

| 指标 | 数量 |
|------|------|
| 培训天数 | 70 天 |
| 每日课件 | ≥ 20,000 字（含旁白、需求、架构图、跟敲指南、FAQ、作业答案） |
| 累计代码 | **103,761+ 行**（课件 + 平台 + 测试 + 数据） |
| 阶段项目 | 4 个（CLI 助手 / Web Chat / 企业知识库 / 多 Agent 办公助手） |
| 协作模拟 | Jira Epic + GitLab MR/CI |

## 开始学习

```bash
cd nexus-agent-bootcamp/courseware/day-01
# 阅读 README.md，按步骤跟敲 code/ 目录下代码
```

## 重新生成课件与平台（讲师）

```bash
cd nexus-agent-bootcamp/scripts
python3 generate_courseware.py   # 生成 70 天课件
python3 build_platform.py        # 构建企业级平台代码库
python3 verify_day.py --day 1    # 验证指定天代码
```

## 许可证

MIT
