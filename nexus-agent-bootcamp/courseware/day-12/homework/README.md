# Day 12 作业

在 `homework/chat_client.py` 中：

1. 封装 `chat_once(prompt: str, system: str = "") -> str`
2. HTTP 5xx 或超时时自动重试 3 次，间隔 2 秒
3. 将每次调用的 usage 追加写入 `usage.log`（JSON Lines 格式）
4. 命令行：`python chat_client.py "你的问题"`


## 答案见

courseware/day-12/README.md 底部
