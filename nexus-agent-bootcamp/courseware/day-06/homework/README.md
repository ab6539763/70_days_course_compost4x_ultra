# Day 6 作业

**作业：抽取 io_utils 模块**

1. 从 Day5 `json_parser` 抽出 `load_json_file` / `save_json_file` 到 `homework/io_utils.py`
2. 新增 `load_json_or_none(path)` 失败返回 None 并打印警告
3. `homework/test_io.py` 调用并断言往返一致
4. 原 json_parser 改为 from io_utils import ...（若在本目录运行需说明 PYTHONPATH）


## 答案见

courseware/day-06/README.md 底部
