#!/usr/bin/env python3
"""
Day 52 — 微调数据集准备
将原始 QA 对转换为 LLaMA-Factory 兼容的 Alpaca JSON 格式
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_alpaca_record(
    instruction: str,
    input_text: str,
    output: str,
    system: str = "你是智链科技 NexusAgent 领域助手。",
) -> dict[str, str]:
    """构造单条 Alpaca 格式训练样本"""
    return {
        "instruction": instruction,
        "input": input_text,
        "output": output,
        "system": system,
    }


def validate_record(record: dict[str, Any]) -> list[str]:
    """校验单条记录，返回错误列表（空列表表示通过）"""
    errors: list[str] = []
    for field in ("instruction", "output"):
        if not record.get(field, "").strip():
            errors.append(f"字段 `{field}` 不能为空")
    # 输出长度 sanity check
    if len(record.get("output", "")) < 10:
        errors.append("output 过短，可能缺乏训练价值")
    return errors


def convert_qa_pairs(raw_pairs: list[dict[str, str]], output_path: Path) -> int:
    """批量转换并写入 JSON 文件，返回有效样本数"""
    valid: list[dict[str, str]] = []
    for i, pair in enumerate(raw_pairs):
        rec = build_alpaca_record(
            instruction=pair.get("question", ""),
            input_text=pair.get("context", ""),
            output=pair.get("answer", ""),
        )
        errs = validate_record(rec)
        if errs:
            print(f"[跳过] 样本 {i}: {errs}")
            continue
        valid.append(rec)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(valid, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已写入 {len(valid)} 条样本 -> {output_path}")
    return len(valid)


# 智链科技客服领域示例数据
SAMPLE_QA = [
    {
        "question": "如何重置 NexusAgent 管理员密码？",
        "context": "管理后台 > 系统设置 > 安全",
        "answer": "登录管理后台，进入「系统设置 > 安全 > 重置密码」，"
        "输入超级管理员邮箱接收验证码后即可重置。若忘记超级管理员账号，请联系运维执行 CLI 重置。",
    },
    {
        "question": "RAG 检索结果为空怎么办？",
        "context": "知识库模块故障排查",
        "answer": "请依次检查：1) 文档是否已完成向量化；2) Chroma 服务是否在线；"
        "3) embedding 模型版本是否与入库时一致；4) 检索 top_k 是否过小。",
    },
]


def main() -> None:
    out = Path("data/nexus_qa_train.json")
    count = convert_qa_pairs(SAMPLE_QA, out)
    assert count >= 2, "至少需要 2 条有效样本"
    print("数据集准备完成，可用于 LLaMA-Factory 训练。")


if __name__ == "__main__":
    main()
