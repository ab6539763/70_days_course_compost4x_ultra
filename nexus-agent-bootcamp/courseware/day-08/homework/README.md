# Day 8 作业

在 `homework/chat_message_ext.py` 中扩展 ChatMessage：

1. 实现 `is_empty()`：判断 content 是否仅含空白字符
2. 实现 `merge(other: ChatMessage) -> ChatMessage`：合并两条同 role 消息（content 用换行拼接）
3. 实现 `format_for_api() -> dict`：仅返回 `{"role": ..., "content": ...}`，供 LLM API 调用
4. 编写 `if __name__ == "__main__"` 演示上述三个方法


## 答案见

courseware/day-08/README.md 底部
