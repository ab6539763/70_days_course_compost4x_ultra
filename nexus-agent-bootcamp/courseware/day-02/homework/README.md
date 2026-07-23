# Day 2 课后作业

## 任务

扩展 `text_cleaner.py`，在 `homework/text_cleaner_hw.py` 中实现：

1. `mask_email(text)` — 邮箱脱敏 `zhangming@smartlink.cn` → `z***@smartlink.cn`
2. `extract_hashtags(text)` — 提取 `#话题` 列表（不含 #）
3. 至少 3 个 `assert` 自测用例
4. 提交 MR：`[Day-02] homework: 文本清洗扩展`

## 运行

```bash
cd courseware/day-02
python3 homework/text_cleaner_hw.py
```

## 参考答案

见 `homework/text_cleaner_hw.py`（请先独立完成再对照）

## 评分标准

| 项 | 分值 |
|----|------|
| 功能完整 | 40 |
| 代码规范与注释 | 30 |
| 异常处理 | 15 |
| MR 与 Jira 关联 | 15 |
