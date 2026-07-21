# NexusAgent 架构演进路线图

## v0.1 → v1.0 演进时间线

```mermaid
gantt
    title NexusAgent 架构演进
    dateFormat  YYYY-MM-DD
    section 基础
    CLI 助手           :d1, 2026-01-01, 14d
    section Web
    FastAPI + SSE      :d2, after d1, 10d
    section RAG
    知识库检索         :d3, after d2, 14d
    section Agent
    LangGraph 编排     :d4, after d3, 12d
    section 生产
    微调 + Docker      :d5, after d4, 10d
    section 毕业
    v1.0 交付          :d6, after d5, 13d
```

## 各版本架构快照

### v0.1 (Day 14) — 单机 CLI

```mermaid
flowchart LR
    USER --> CLI[cli_chat_assistant]
    CLI --> JSON[(history.json)]
    CLI --> API[DeepSeek API]
```

### v0.3 (Day 38) — RAG 知识库

```mermaid
flowchart TB
    DOC[文档上传] --> INGEST[分割+向量化]
    INGEST --> CHROMA[(Chroma)]
    QUERY[用户问题] --> RETRIEVE[混合检索+重排]
    RETRIEVE --> CHROMA
    RETRIEVE --> LLM[大模型生成]
    LLM --> ANSWER[带引用答案]
```

### v1.0 (Day 70) — 完整企业平台

见 [project-master-plan.md](./project-master-plan.md) 最终架构图。

## 技术选型决策记录 (ADR)

| ADR | 决策 | 原因 |
|-----|------|------|
| ADR-001 | Python 3.10+ | 类型注解、match 语句 |
| ADR-002 | FastAPI | 异步、自动文档、Pydantic |
| ADR-003 | Chroma 教学 / Milvus 生产 | 易学 + 可扩展 |
| ADR-004 | LangGraph Agent 编排 | 状态机、人工审批 |
| ADR-005 | Docker Compose 部署 | 学员可复现 |
