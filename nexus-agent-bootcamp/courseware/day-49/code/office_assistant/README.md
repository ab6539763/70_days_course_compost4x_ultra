# 多 Agent 办公助手（Day 48-49）

## Agent 分工
- **Researcher**: 知识检索
- **Writer**: 文档撰写
- **Scheduler**: 会议安排

## 运行
```bash
python main.py "写项目周报邮件"
uvicorn api:app --app-dir office_assistant --reload
```
