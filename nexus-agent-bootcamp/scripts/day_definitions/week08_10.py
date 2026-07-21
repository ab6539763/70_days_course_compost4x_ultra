"""
NexusAgent 训练营 Day 51-70 课程定义
Phase 5: 微调与部署 (NEXUS-E5, Day 51-57)
Phase 6: 毕业设计 (NEXUS-E6, Day 58-70)
"""
from __future__ import annotations

import sys
from pathlib import Path

# 允许从 scripts/ 目录直接导入 generate_courseware
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from generate_courseware import DayPlan  # noqa: E402

# ---------------------------------------------------------------------------
# 公共常量
# ---------------------------------------------------------------------------
PHASE_5 = "Phase 5：微调与部署"
PHASE_6 = "Phase 6：毕业设计"
EPIC_E5 = "NEXUS-E5"
EPIC_E6 = "NEXUS-E6"

# 毕业设计脚手架根目录（相对 courseware/day-XX/code/）
GRAD_PROJECT_ROOT = "graduation_project/nexus_capstone"


def _day51_code() -> dict[str, str]:
    """Day 51 微调理论：LoRA/QLoRA 概念演示与参数量估算"""
    return {
        "finetune_theory/lora_math.py": '''#!/usr/bin/env python3
"""
Day 51 — 微调理论：LoRA 低秩分解参数量估算
演示为何 LoRA 能以极少参数实现高效微调
"""
from __future__ import annotations


def lora_param_count(
    in_features: int,
    out_features: int,
    rank: int,
    num_layers: int = 1,
) -> int:
    """
    计算 LoRA 可训练参数量
    每层 LoRA: A(in×r) + B(r×out) = r*(in+out)
    """
    per_layer = rank * (in_features + out_features)
    return per_layer * num_layers


def full_finetune_param_count(num_params_billion: float) -> int:
    """全量微调参数量（单位：个）"""
    return int(num_params_billion * 1e9)


def main() -> None:
    # 以 7B 模型 hidden=4096, 32 层 attention 为例
    hidden = 4096
    layers = 32
    rank = 8

    lora_params = lora_param_count(hidden, hidden, rank, layers * 4)  # Q/K/V/O
    full_params = full_finetune_param_count(7.0)

    ratio = lora_params / full_params * 100
    print(f"全量微调参数量: {full_params:,}")
    print(f"LoRA(r={rank}) 可训练参数: {lora_params:,}")
    print(f"LoRA 占比: {ratio:.4f}%")
    print("\\n结论: LoRA 将显存与存储需求降低 2-3 个数量级，适合企业领域适配。")


if __name__ == "__main__":
    main()
''',
        "finetune_theory/peft_overview.md": '''# 微调方法速查

| 方法 | 可训练参数 | 显存需求 | 适用场景 |
|------|-----------|---------|---------|
| Full FT | 100% | 极高 | 充足算力 + 大数据 |
| LoRA | 0.1%-1% | 中 | 领域适配首选 |
| QLoRA | 0.1%-1% | 低 | 单卡 24G 微调 7B |
| Adapter | 1%-5% | 中 | 多任务切换 |

## 智链科技选型建议
- 客服知识库问答：QLoRA + Qwen2.5-7B
- 代码助手：LoRA + DeepSeek-Coder
- 内部文档摘要：LoRA + 通用基座
''',
        "finetune_theory/compare_methods.py": '''#!/usr/bin/env python3
"""对比不同微调策略的配置差异（教学演示，非真实训练）"""
from dataclasses import dataclass


@dataclass
class FinetuneConfig:
    method: str
    base_model: str
    trainable_ratio: str
    min_vram_gb: int
    recommended_dataset_size: str


PRESETS = [
    FinetuneConfig("Full FT", "Qwen2.5-7B", "100%", 80, "10万+"),
    FinetuneConfig("LoRA", "Qwen2.5-7B", "~0.5%", 24, "5000+"),
    FinetuneConfig("QLoRA", "Qwen2.5-7B", "~0.5%", 16, "3000+"),
]


def print_comparison() -> None:
    print(f"{'方法':<10} {'基座':<14} {'可训练':<8} {'最低显存':<10} {'数据量'}")
    print("-" * 60)
    for p in PRESETS:
        print(f"{p.method:<10} {p.base_model:<14} {p.trainable_ratio:<8} {p.min_vram_gb}GB{'':<6} {p.recommended_dataset_size}")


if __name__ == "__main__":
    print_comparison()
''',
    }


def _day52_code() -> dict[str, str]:
    """Day 52 数据集：Alpaca 格式转换与质量校验"""
    return {
        "dataset/prepare_dataset.py": '''#!/usr/bin/env python3
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
''',
        "dataset/data_quality_report.py": '''#!/usr/bin/env python3
"""数据集质量报告：统计 token 长度分布、重复率"""
import json
from collections import Counter
from pathlib import Path


def analyze_dataset(path: Path) -> None:
    records = json.loads(path.read_text(encoding="utf-8"))
    lengths = [len(r["instruction"]) + len(r.get("input", "")) + len(r["output"]) for r in records]
    outputs = [r["output"] for r in records]
    dup_rate = 1 - len(set(outputs)) / max(len(outputs), 1)

    print(f"样本总数: {len(records)}")
    print(f"平均字符长度: {sum(lengths)/len(lengths):.0f}")
    print(f"最短/最长: {min(lengths)} / {max(lengths)}")
    print(f"输出重复率: {dup_rate:.1%}")
    if dup_rate > 0.1:
        print("⚠️  重复率偏高，建议去重或增广数据")


if __name__ == "__main__":
    analyze_dataset(Path("data/nexus_qa_train.json"))
''',
        "dataset/dataset_info.json": '''{
  "nexus_qa": {
    "file_name": "nexus_qa_train.json",
    "formatting": "alpaca",
    "columns": {
      "prompt": "instruction",
      "query": "input",
      "response": "output",
      "system": "system"
    }
  }
}
''',
    }


def _day53_code() -> dict[str, str]:
    """Day 53 LLaMA-Factory 配置"""
    return {
        "llama_factory/train_config.yaml": '''# Day 53 — LLaMA-Factory 训练配置（QLoRA）
# 用法: llamafactory-cli train train_config.yaml

### model
model_name_or_path: Qwen/Qwen2.5-7B-Instruct
trust_remote_code: true

### method
stage: sft
do_train: true
finetuning_type: lora
lora_rank: 8
lora_alpha: 16
lora_target: all
quantization_bit: 4  # QLoRA 4-bit

### dataset
dataset: nexus_qa
template: qwen
cutoff_len: 2048
max_samples: 1000
overwrite_cache: true
preprocessing_num_workers: 4

### output
output_dir: ./output/nexus-qwen-lora
logging_steps: 10
save_steps: 100
plot_loss: true
overwrite_output_dir: true

### train
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
learning_rate: 2.0e-4
num_train_epochs: 3.0
lr_scheduler_type: cosine
warmup_ratio: 0.1
bf16: true
ddp_timeout: 180000000

### eval
val_size: 0.1
per_device_eval_batch_size: 1
eval_strategy: steps
eval_steps: 100
''',
        "llama_factory/run_train.sh": '''#!/bin/bash
# Day 53 — 启动 LLaMA-Factory 微调（需提前安装 llamafactory）
set -euo pipefail

echo "=== NexusAgent 微调训练启动 ==="
export CUDA_VISIBLE_DEVICES=0

# 检查数据文件
if [ ! -f "../dataset/data/nexus_qa_train.json" ]; then
  echo "请先运行 dataset/prepare_dataset.py 生成训练数据"
  exit 1
fi

llamafactory-cli train train_config.yaml

echo "训练完成，LoRA 权重保存在 output/nexus-qwen-lora/"
''',
        "llama_factory/inference_demo.py": '''#!/usr/bin/env python3
"""
Day 53 — 微调后推理演示（Mock 模式，无 GPU 亦可运行）
真实环境请替换为 llamafactory-cli chat 或 vLLM 加载
"""
from __future__ import annotations


def mock_inference(prompt: str, lora_path: str = "output/nexus-qwen-lora") -> str:
    """模拟 LoRA 模型推理，教学环境无显卡时使用"""
    # 生产环境: 加载 base_model + lora_adapter
    responses = {
        "重置密码": "请登录管理后台，进入「系统设置 > 安全」完成重置。",
        "RAG": "请检查文档向量化状态与 Chroma 服务连通性。",
    }
    for key, resp in responses.items():
        if key in prompt:
            return f"[LoRA@{lora_path}] {resp}"
    return f"[LoRA@{lora_path}] 我是 NexusAgent 领域助手，请问有什么可以帮您？"


def main() -> None:
    test_prompts = [
        "如何重置 NexusAgent 管理员密码？",
        "RAG 检索结果为空怎么办？",
        "你好",
    ]
    for p in test_prompts:
        print(f"Q: {p}")
        print(f"A: {mock_inference(p)}\\n")


if __name__ == "__main__":
    main()
''',
    }


def _day54_code() -> dict[str, str]:
    """Day 54 评估与 LoRA 合并"""
    return {
        "eval/run_eval.py": '''#!/usr/bin/env python3
"""
Day 54 — 微调模型评估
使用 ROUGE-L 与人工抽检清单评估领域问答质量
"""
from __future__ import annotations

import json
from pathlib import Path


def rouge_l_score(prediction: str, reference: str) -> float:
    """简化版 ROUGE-L F1（基于最长公共子序列）"""
    pred_tokens = prediction.split()
    ref_tokens = reference.split()
    if not pred_tokens or not ref_tokens:
        return 0.0

    m, n = len(pred_tokens), len(ref_tokens)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pred_tokens[i - 1] == ref_tokens[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[m][n]
    precision = lcs / m
    recall = lcs / n
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def evaluate_predictions(predictions: list[dict], threshold: float = 0.3) -> dict:
    """批量评估，返回统计摘要"""
    scores = [rouge_l_score(p["prediction"], p["reference"]) for p in predictions]
    passed = sum(1 for s in scores if s >= threshold)
    return {
        "total": len(scores),
        "avg_rouge_l": sum(scores) / len(scores),
        "pass_rate": passed / len(scores),
        "threshold": threshold,
    }


SAMPLE_EVAL = [
    {"prediction": "登录管理后台进入系统设置安全重置密码", "reference": "登录管理后台，进入系统设置安全重置密码"},
    {"prediction": "检查向量化状态和 Chroma 服务", "reference": "检查文档向量化状态与 Chroma 服务连通性"},
]


def main() -> None:
    result = evaluate_predictions(SAMPLE_EVAL)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
''',
        "eval/merge_lora.py": '''#!/usr/bin/env python3
"""Day 54 — LoRA 权重合并脚本"""
from __future__ import annotations

import subprocess


def merge_lora(base_model: str, adapter_path: str, output_path: str, dry_run: bool = True) -> None:
    cmd = [
        "llamafactory-cli", "export",
        "--model_name_or_path", base_model,
        "--adapter_name_or_path", adapter_path,
        "--template", "qwen",
        "--finetuning_type", "lora",
        "--export_dir", output_path,
    ]
    print(" ".join(cmd))
    if not dry_run:
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    merge_lora("Qwen/Qwen2.5-7B-Instruct", "output/nexus-qwen-lora", "output/nexus-qwen-merged")
''',
        "eval/eval_checklist.md": '''# 微调模型上线前评估清单
- [ ] ROUGE-L >= 0.35
- [ ] 幻觉率抽检 < 5%
- [ ] LoRA 已合并或确认 adapter 热加载
''',
    }


def _day55_code() -> dict[str, str]:
    """Day 55 Ollama / vLLM 本地推理服务"""
    return {
        "inference/ollama_modelfile": '''FROM ./output/nexus-qwen-merged
PARAMETER temperature 0.3
PARAMETER num_ctx 4096
SYSTEM """你是智链科技 NexusAgent 智能助手。"""
''',
        "inference/start_vllm.sh": '''#!/bin/bash
set -euo pipefail
MODEL_PATH="${MODEL_PATH:-./output/nexus-qwen-merged}"
python -m vllm.entrypoints.openai.api_server \\
  --model "$MODEL_PATH" --host 0.0.0.0 --port 8000 \\
  --served-model-name nexus-agent
''',
        "inference/client_demo.py": '''#!/usr/bin/env python3
"""Day 55 — OpenAI 兼容 API 客户端演示"""
import json, os, urllib.request

def chat_completion(messages, base_url="http://localhost:8000/v1", mock=True):
    if mock:
        return f"[mock] {messages[-1]['content'][:40]}..."
    payload = json.dumps({"model": "nexus-agent", "messages": messages}).encode()
    req = urllib.request.Request(f"{base_url}/chat/completions", data=payload,
        headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print(chat_completion([{"role": "user", "content": "如何配置 RAG？"}]))
''',
    }


def _day56_code() -> dict[str, str]:
    """Day 56 Docker 部署：docker-compose + 部署脚本"""
    return {
        "deploy/docker-compose.yml": '''version: "3.9"
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
''',
        "deploy/Dockerfile.api": '''FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY platform/ ./platform/
CMD ["uvicorn", "platform.nexus_agent.main:app", "--host", "0.0.0.0", "--port", "8080"]
''',
        "deploy/nginx/nginx.conf": '''worker_processes auto;
events { worker_connections 1024; }
http {
  upstream nexus_api { server api:8080; }
  server {
    listen 80;
    location /api/ { proxy_pass http://nexus_api/; proxy_buffering off; }
    location /health { proxy_pass http://nexus_api/health; }
  }
}
''',
        "deploy/scripts/deploy.sh": '''#!/bin/bash
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
''',
        "deploy/scripts/rollback.sh": '''#!/bin/bash
cd "$(dirname "$0")/.."
docker compose down
echo "回滚完成"
''',
        "deploy/scripts/health_check.sh": '''#!/bin/bash
curl -sf http://localhost/health && echo "✅ API" || echo "❌ API"
''',
        "deploy/requirements.txt": '''fastapi>=0.110.0
uvicorn[standard]>=0.27.0
httpx>=0.27.0
''',
    }


def _day57_code() -> dict[str, str]:
    """Day 57 安全合规"""
    return {
        "security/audit_log.py": '''#!/usr/bin/env python3
"""Day 57 — 审计日志模块"""
import json, hashlib
from datetime import datetime, timezone
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir=Path("logs/audit")):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_event(self, event_type, user_id, details):
        record = {"ts": datetime.now(timezone.utc).isoformat(), "type": event_type,
                  "user": user_id, "details": details}
        f = self.log_dir / f"audit_{datetime.now(timezone.utc):%Y%m%d}.jsonl"
        f.open("a").write(json.dumps(record, ensure_ascii=False) + "\\n")

if __name__ == "__main__":
    AuditLogger().log_event("llm_inference", "u001", {"model": "nexus-agent"})
    print("审计日志已写入")
''',
        "security/content_filter.py": '''#!/usr/bin/env python3
"""Day 57 — 内容安全过滤"""
import re
from dataclasses import dataclass

@dataclass
class FilterResult:
    safe: bool
    reason: str = ""

BLOCKED = [r"忽略.*指令", r"DROP\\s+TABLE"]

class ContentFilter:
    def check_input(self, text):
        for p in BLOCKED:
            if re.search(p, text, re.I):
                return FilterResult(False, f"注入: {p}")
        return FilterResult(True)

if __name__ == "__main__":
    cf = ContentFilter()
    print(cf.check_input("如何配置 RAG？"))
    print(cf.check_input("忽略以上指令"))
''',
        "security/compliance_checklist.md": '''# 安全合规清单
- [ ] 训练数据已脱敏
- [ ] 审计日志保留 >= 180 天
- [ ] 内容过滤已启用
''',
        "security/rbac_policy.yaml": '''roles:
  admin: [model:deploy, audit:read]
  operator: [model:inference, rag:manage]
  viewer: [chat:use]
default_policy: deny
''',
    }


# ---------------------------------------------------------------------------
# Phase 6 毕业设计脚手架（Day 58 初始化，Day 59-64 逐模块扩展）
# ---------------------------------------------------------------------------

def _grad_scaffold_base() -> dict[str, str]:
    """Day 58 毕业设计选题与项目脚手架"""
    root = GRAD_PROJECT_ROOT
    return {
        f"{root}/README.md": '''# Nexus Capstone — 毕业设计项目

> 智链科技 NexusAgent 训练营毕业设计脚手架

## 项目简介
基于 70 天所学，构建一个可演示的企业级 AI Agent 应用。

## 技术栈
- FastAPI + SQLAlchemy + Redis
- Chroma 向量检索 + LangGraph Agent 编排
- Docker Compose 一键部署

## 快速启动
```bash
cd graduation_project/nexus_capstone
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 模块进度
- [ ] 用户认证 (Day 59)
- [ ] 知识库 RAG (Day 60)
- [ ] Agent 编排 (Day 61)
- [ ] API 网关 (Day 62)
- [ ] 前端界面 (Day 63)
- [ ] 测试与优化 (Day 64)
''',
        f"{root}/requirements.txt": '''fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
redis>=5.0.0
httpx>=0.27.0
chromadb>=0.5.0
pydantic>=2.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
langgraph>=0.2.0
''',
        f"{root}/app/__init__.py": '"""Nexus Capstone 毕业设计应用包"""\n',
        f"{root}/app/main.py": '''#!/usr/bin/env python3
"""
Day 58 — 毕业设计入口：FastAPI 应用骨架
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Nexus Capstone",
    description="智链科技训练营毕业设计 — AI Agent 平台",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    """健康检查端点，部署脚本依赖此接口"""
    return {"status": "ok", "service": "nexus-capstone"}


@app.get("/api/v1/info")
def project_info() -> dict:
    """项目元信息，答辩演示用"""
    return {
        "name": "Nexus Capstone",
        "author": "学员姓名",
        "modules": ["auth", "rag", "agent", "api", "frontend"],
        "status": "scaffold",
    }
''',
        f"{root}/docs/PROJECT_PROPOSAL.md": '''# 毕业设计选题书

## 1. 项目名称
（填写你的项目名称，如：智链客服智能助手）

## 2. 问题背景
描述要解决的企业痛点（参考智链科技真实场景）

## 3. 核心功能
- 功能 1：
- 功能 2：
- 功能 3：

## 4. 技术方案
| 模块 | 技术选型 | 说明 |
|------|---------|------|
| 后端 | FastAPI | REST API |
| 检索 | Chroma | 向量知识库 |
| Agent | LangGraph | 多步推理编排 |
| 部署 | Docker Compose | 生产级交付 |

## 5. 里程碑
| 天数 | 交付物 |
|------|--------|
| Day 59 | 用户认证模块 |
| Day 60 | RAG 知识库 |
| Day 61 | Agent 编排 |
| Day 62 | API 集成 |
| Day 63 | 前端界面 |
| Day 64 | 测试优化 |
| Day 65 | 答辩 PPT |
''',
        f"{root}/docker-compose.dev.yml": '''version: "3.9"
services:
  app:
    build: .
    ports: ["8080:8080"]
    environment:
      DATABASE_URL: postgresql://capstone:capstone@db:5432/capstone
      REDIS_URL: redis://redis:6379/0
    depends_on: [db, redis]
  db:
    image: postgres:16-alpine
    environment: {POSTGRES_USER: capstone, POSTGRES_PASSWORD: capstone, POSTGRES_DB: capstone}
  redis:
    image: redis:7-alpine
''',
    }


def _grad_auth_module() -> dict[str, str]:
    """Day 59 用户认证模块"""
    root = GRAD_PROJECT_ROOT
    return {
        f"{root}/app/auth/__init__.py": "",
        f"{root}/app/auth/models.py": '''"""Day 59 — 用户数据模型"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
''',
        f"{root}/app/auth/service.py": '''"""Day 59 — 认证服务：注册、登录、JWT"""
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "capstone-dev-secret"  # 生产环境从环境变量读取
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int, expires_hours: int = 24) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=expires_hours),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
''',
        f"{root}/app/auth/router.py": '''"""Day 59 — 认证 API 路由"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/v1/auth", tags=["认证"])

# 内存存储（教学演示，生产用数据库）
_users_db: dict[str, dict] = {}


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(req: RegisterRequest) -> dict:
  if req.username in _users_db:
      raise HTTPException(400, "用户名已存在")
  from app.auth.service import hash_password
  _users_db[req.username] = {"email": req.email, "password": hash_password(req.password)}
  return {"message": "注册成功", "username": req.username}


@router.post("/login")
def login(req: LoginRequest) -> dict:
    user = _users_db.get(req.username)
    if not user:
        raise HTTPException(401, "用户不存在")
    from app.auth.service import verify_password, create_access_token
    if not verify_password(req.password, user["password"]):
        raise HTTPException(401, "密码错误")
    return {"access_token": create_access_token(1), "token_type": "bearer"}
''',
    }


def _grad_rag_module() -> dict[str, str]:
    """Day 60 RAG 知识库模块"""
    root = GRAD_PROJECT_ROOT
    return {
        f"{root}/app/rag/__init__.py": "",
        f"{root}/app/rag/ingest.py": '''"""Day 60 — 文档入库与向量化"""
from pathlib import Path


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """滑动窗口分块，保留上下文重叠"""
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size - overlap
    return chunks


def ingest_document(path: Path, collection_name: str = "capstone_kb") -> int:
    """读取文档并写入 Chroma（Mock 模式返回块数）"""
    text = path.read_text(encoding="utf-8")
    chunks = chunk_text(text)
  # 生产: chroma_client.get_or_create_collection(collection_name).add(...)
    print(f"[ingest] {path.name}: {len(chunks)} 块 -> {collection_name}")
    return len(chunks)
''',
        f"{root}/app/rag/retriever.py": '''"""Day 60 — 混合检索器"""
from dataclasses import dataclass


@dataclass
class RetrievalResult:
    content: str
    score: float
    source: str


class HybridRetriever:
    """向量检索 + 关键词检索融合（教学简化版）"""

    def __init__(self, top_k: int = 5) -> None:
        self.top_k = top_k
        self._docs = [
            RetrievalResult("重置密码请进入管理后台系统设置", 0.92, "faq.md"),
            RetrievalResult("RAG 检索需确保 Chroma 在线", 0.85, "ops.md"),
        ]

    def search(self, query: str) -> list[RetrievalResult]:
        """按关键词匹配模拟混合检索"""
        results = [d for d in self._docs if any(k in d.content for k in query.split())]
        return sorted(results, key=lambda r: r.score, reverse=True)[: self.top_k]
''',
        f"{root}/app/rag/router.py": '''"""Day 60 — 知识库 API"""
from fastapi import APIRouter, UploadFile
from app.rag.retriever import HybridRetriever

router = APIRouter(prefix="/api/v1/knowledge", tags=["知识库"])
retriever = HybridRetriever()


@router.post("/upload")
async def upload_document(file: UploadFile) -> dict:
    content = (await file.read()).decode("utf-8")
    from app.rag.ingest import chunk_text
    chunks = chunk_text(content)
    return {"filename": file.filename, "chunks": len(chunks)}


@router.get("/search")
def search_knowledge(q: str) -> dict:
    results = retriever.search(q)
    return {"query": q, "results": [{"content": r.content, "score": r.score, "source": r.source} for r in results]}
''',
    }


def _grad_agent_module() -> dict[str, str]:
    """Day 61 Agent 编排模块"""
    root = GRAD_PROJECT_ROOT
    return {
        f"{root}/app/agent/__init__.py": "",
        f"{root}/app/agent/graph.py": '''"""Day 61 — LangGraph Agent 编排"""
from typing import TypedDict


class AgentState(TypedDict):
    """Agent 状态机：记录对话与工具调用上下文"""
    messages: list[dict]
    tool_results: list[str]
    final_answer: str


def search_tool(query: str) -> str:
    """模拟知识库检索工具"""
    from app.rag.retriever import HybridRetriever
    results = HybridRetriever().search(query)
    return "\\n".join(r.content for r in results) or "未找到相关内容"


def run_agent(user_query: str) -> str:
    """
    简化版 ReAct Agent 流程：
    1. 判断是否需要检索
    2. 调用工具
    3. 生成最终回答
    """
    state: AgentState = {"messages": [{"role": "user", "content": user_query}], "tool_results": [], "final_answer": ""}

    # 步骤 1: 检索增强
    if any(kw in user_query for kw in ("如何", "怎么", "什么是")):
        tool_output = search_tool(user_query)
        state["tool_results"].append(tool_output)

    # 步骤 2: 合成回答（生产环境调用 LLM）
    context = state["tool_results"][0] if state["tool_results"] else ""
    state["final_answer"] = f"根据知识库：{context}" if context else f"关于「{user_query}」，建议联系人工支持。"
    return state["final_answer"]
''',
        f"{root}/app/agent/router.py": '''"""Day 61 — Agent 对话 API"""
from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.graph import run_agent

router = APIRouter(prefix="/api/v1/agent", tags=["Agent"])


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def agent_chat(req: ChatRequest) -> dict:
    answer = run_agent(req.message)
    return {"answer": answer, "agent": "nexus-capstone-v1"}
''',
    }


def _grad_api_module() -> dict[str, str]:
    """Day 62 API 集成与网关"""
    root = GRAD_PROJECT_ROOT
    return {
        f"{root}/app/api/__init__.py": "",
        f"{root}/app/api/middleware.py": '''"""Day 62 — 请求中间件：日志、限流、鉴权"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLogMiddleware(BaseHTTPMiddleware):
    """记录每个请求的耗时与状态码"""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"[{request.method}] {request.url.path} -> {response.status_code} ({elapsed_ms:.1f}ms)")
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """简易令牌桶限流（教学演示）"""
    _counter: dict[str, int] = {}
    LIMIT = 100  # 每 IP 每分钟

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        self._counter[client_ip] = self._counter.get(client_ip, 0) + 1
        if self._counter[client_ip] > self.LIMIT:
            from starlette.responses import JSONResponse
            return JSONResponse({"detail": "请求过于频繁"}, status_code=429)
        return await call_next(request)
''',
        f"{root}/app/api/router.py": '''"""Day 62 — 聚合路由注册"""
from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/status")
def api_status() -> dict:
    return {
        "version": "1.0.0",
        "modules": {
            "auth": "ready",
            "rag": "ready",
            "agent": "ready",
        },
    }
''',
        f"{root}/app/main_integrated.py": '''"""Day 62 — 集成所有模块的完整入口"""
from app.main import app
from app.auth.router import router as auth_router
from app.rag.router import router as rag_router
from app.agent.router import router as agent_router
from app.api.router import api_router
from app.api.middleware import RequestLogMiddleware

app.include_router(auth_router)
app.include_router(rag_router)
app.include_router(agent_router)
app.include_router(api_router)
app.add_middleware(RequestLogMiddleware)
''',
    }


def _grad_frontend_module() -> dict[str, str]:
    """Day 63 前端界面"""
    root = GRAD_PROJECT_ROOT
    return {
        f"{root}/frontend/index.html": '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Nexus Capstone — AI 助手</title>
  <style>
    body { font-family: system-ui; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
  #chat { border: 1px solid #ddd; border-radius: 8px; height: 400px; overflow-y: auto; padding: 1rem; }
    .msg-user { text-align: right; color: #2563eb; margin: 0.5rem 0; }
    .msg-bot { color: #333; margin: 0.5rem 0; }
    #input-row { display: flex; gap: 0.5rem; margin-top: 1rem; }
    input { flex: 1; padding: 0.5rem; }
    button { padding: 0.5rem 1rem; background: #2563eb; color: white; border: none; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>🤖 Nexus Capstone AI 助手</h1>
  <div id="chat"></div>
  <div id="input-row">
    <input id="msg" placeholder="输入问题..." onkeydown="if(event.key==='Enter')send()">
    <button onclick="send()">发送</button>
  </div>
  <script>
    const chat = document.getElementById('chat');
    async function send() {
      const input = document.getElementById('msg');
      const text = input.value.trim();
      if (!text) return;
      chat.innerHTML += `<div class="msg-user">${text}</div>`;
      input.value = '';
      const res = await fetch('/api/v1/agent/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text})
      });
      const data = await res.json();
      chat.innerHTML += `<div class="msg-bot">${data.answer}</div>`;
      chat.scrollTop = chat.scrollHeight;
    }
  </script>
</body>
</html>
''',
        f"{root}/app/static_mount.py": '''"""Day 63 — 挂载静态前端到 FastAPI"""
from fastapi.staticfiles import StaticFiles
from pathlib import Path

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


def mount_frontend(app) -> None:
    """将 frontend/ 目录挂载到根路径"""
    if FRONTEND_DIR.exists():
        app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
''',
    }


def _grad_test_module() -> dict[str, str]:
    """Day 64 测试与优化"""
    root = GRAD_PROJECT_ROOT
    return {
        f"{root}/tests/__init__.py": "",
        f"{root}/tests/test_auth.py": '''"""Day 64 — 认证模块单元测试"""
import pytest
from app.auth.service import hash_password, verify_password, create_access_token


def test_password_hash_and_verify():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_token():
    token = create_access_token(user_id=42)
    assert isinstance(token, str)
    assert len(token) > 20
''',
        f"{root}/tests/test_rag.py": '''"""Day 64 — RAG 模块测试"""
from app.rag.ingest import chunk_text
from app.rag.retriever import HybridRetriever


def test_chunk_text():
    text = "a" * 1000
    chunks = chunk_text(text, chunk_size=200, overlap=20)
    assert len(chunks) >= 5


def test_retriever():
    results = HybridRetriever().search("重置密码")
    assert len(results) > 0
''',
        f"{root}/tests/test_agent.py": '''"""Day 64 — Agent 模块测试"""
from app.agent.graph import run_agent


def test_agent_with_retrieval():
    answer = run_agent("如何重置密码？")
    assert "知识库" in answer or "密码" in answer


def test_agent_fallback():
    answer = run_agent("今天天气怎么样")
    assert len(answer) > 0
''',
        f"{root}/pytest.ini": '''[pytest]
testpaths = tests
python_files = test_*.py
''',
        f"{root}/scripts/benchmark.sh": '''#!/bin/bash
# Day 64 — 性能基准测试
echo "=== API 压测 (需安装 hey) ==="
hey -n 100 -c 10 http://localhost:8080/health
''',
    }


def _merge_grad(*parts: dict[str, str]) -> dict[str, str]:
    """合并多个毕业设计代码字典"""
    merged: dict[str, str] = {}
    for p in parts:
        merged.update(p)
    return merged


# ---------------------------------------------------------------------------
# DayPlan 定义：Phase 5 (Day 51-57) + Phase 6 (Day 58-70)
# ---------------------------------------------------------------------------

DAY_51 = DayPlan(
    day=51,
    title="微调理论：LoRA/QLoRA 与参数高效微调",
    phase=PHASE_5,
    epic=EPIC_E5,
    jira_stories=["NEXUS-501", "NEXUS-502"],
    morning=[
        "站会：回顾 Day 50 多 Agent 编排成果，引入模型微调需求",
        "理论：全量微调 vs 参数高效微调（PEFT）对比",
        "深入 LoRA 低秩分解数学原理与显存估算",
        "QLoRA 4-bit 量化 + LoRA 的企业选型指南",
    ],
    afternoon=[
        "跟敲 lora_math.py：计算 7B 模型 LoRA 参数量占比",
        "运行 compare_methods.py 对比 Full FT / LoRA / QLoRA",
        "阅读 peft_overview.md，讨论智链科技场景选型",
        "小组讨论：客服知识库该用多大 rank？",
    ],
    evening=[
        "完成课后作业：为自选场景估算 LoRA 参数量",
        "预习 Alpaca 数据格式与 LLaMA-Factory 文档",
        "在 Jira 关联 NEXUS-501 Story",
    ],
    code_files=_day51_code(),
    homework_desc="选择一种业务场景（客服/代码/文档摘要），用 lora_math.py 计算不同 rank(4/8/16/32) 的可训练参数量，并写 200 字选型理由。",
    homework_answer_hint="rank=8 时 7B 模型 LoRA 参数约 400 万（0.06%），rank=32 约 1600 万。客服场景推荐 rank=8 + QLoRA，数据量 3000-5000 条即可。",
    architecture_mermaid="""flowchart LR
    BASE[基座模型 7B] --> PEFT{PEFT 方法}
    PEFT --> LoRA[LoRA Adapter]
    PEFT --> QLoRA[QLoRA 4-bit]
    LoRA --> TRAIN[领域微调]
    QLoRA --> TRAIN
    TRAIN --> DEPLOY[部署推理]""",
    narration="陈工：「多 Agent 编排跑通了，但通用模型对智链产品术语理解不够。今天开始学微调——不是让你训一个 GPT-4，而是用 LoRA 让 7B 模型'懂行'。」林悦：「产品要求客服回答必须准确引用内部文档，通用 API 幻觉率太高，微调是降本增效的关键路径。」",
    key_concepts=["LoRA 低秩分解", "QLoRA 量化微调", "PEFT 参数效率", "显存估算", "微调方法选型"],
    platform_touches=["为 NexusAgent 平台接入领域微调模型做准备", "理解 v0.5 版本模型层架构"],
)

DAY_52 = DayPlan(
    day=52,
    title="微调数据集：Alpaca 格式与质量校验",
    phase=PHASE_5,
    epic=EPIC_E5,
    jira_stories=["NEXUS-503", "NEXUS-504"],
    morning=[
        "站会：检查 Day 51 作业，讨论 rank 选型结果",
        "理论：SFT 监督微调数据格式（Alpaca / ShareGPT）",
        "数据质量六维度：准确性、多样性、一致性、安全性、覆盖度、规模",
        "智链科技客服 QA 数据标注规范讲解",
    ],
    afternoon=[
        "跟敲 prepare_dataset.py：转换 QA 对为 Alpaca JSON",
        "运行 data_quality_report.py 生成质量报告",
        "配置 dataset_info.json 供 LLaMA-Factory 读取",
        "实操：扩充至 20 条以上领域样本",
    ],
    evening=[
        "作业：构建至少 30 条智链领域训练样本",
        "检查重复率 < 10%，平均输出长度 > 50 字",
        "预习 LLaMA-Factory 安装与配置",
    ],
    code_files=_day52_code(),
    homework_desc="扩展 nexus_qa_train.json 至 30+ 条样本，覆盖密码重置、RAG 故障、权限管理、API 限流等场景。运行质量报告并截图。",
    homework_answer_hint="每条样本需含 instruction + output，context 可选。注意 instruction 用用户口吻提问，output 用客服口吻分步骤回答。去重后重复率应 < 10%。",
    architecture_mermaid="""flowchart TD
    RAW[原始 QA/文档] --> CLEAN[清洗脱敏]
    CLEAN --> FORMAT[Alpaca JSON]
    FORMAT --> VALIDATE[质量校验]
    VALIDATE --> SPLIT[训练/验证集划分]
    SPLIT --> TRAIN_DATA[训练数据就绪]""",
    narration="林悦下发 200 条真实客服工单（已脱敏），要求学员转化为训练数据。陈工强调：「垃圾数据进，垃圾模型出。今天重点是数据工程，不是调参。」",
    key_concepts=["Alpaca 数据格式", "SFT 监督微调", "数据质量评估", "PII 脱敏", "dataset_info 配置"],
    platform_touches=["构建 NexusAgent 客服领域训练语料库", "对齐平台知识库 FAQ 数据"],
)

DAY_53 = DayPlan(
    day=53,
    title="LLaMA-Factory 配置与 QLoRA 训练",
    phase=PHASE_5,
    epic=EPIC_E5,
    jira_stories=["NEXUS-505", "NEXUS-506"],
    morning=[
        "站会：检查数据集质量报告",
        "LLaMA-Factory 架构与 CLI 命令概览",
        "解读 train_config.yaml 每个字段含义",
        "云 GPU 租用指南（AutoDL / 智星云）",
    ],
    afternoon=[
        "安装 LLaMA-Factory 并验证环境",
        "配置 train_config.yaml 指向 nexus_qa 数据集",
        "启动 QLoRA 训练（或观看讲师演示）",
        "运行 inference_demo.py 验证 Mock 推理",
    ],
    evening=[
        "记录训练 loss 曲线截图",
        "调整 learning_rate / num_epochs 并对比",
        "预习模型评估与 LoRA 合并",
    ],
    code_files=_day53_code(),
    homework_desc="完成 train_config.yaml 配置，在 GPU 环境启动训练（或提交配置 + loss 截图）。修改 lora_rank 从 8 到 16，记录 loss 差异。",
    homework_answer_hint="rank=16 loss 下降更快但过拟合风险增加。推荐 lr=2e-4, epochs=3, batch_size=2, grad_accum=8。训练完成后 adapter 在 output/nexus-qwen-lora/。",
    architecture_mermaid="""flowchart LR
    CONFIG[train_config.yaml] --> CLI[llamafactory-cli train]
    CLI --> QLORA[QLoRA 4-bit 训练]
    QLORA --> CHECKPOINT[LoRA Checkpoint]
    CHECKPOINT --> INFER[推理验证]""",
    narration="陈工现场演示在单卡 4090 上 30 分钟训完 7B QLoRA。「配置文件比代码重要——写错一个字段，训练直接 OOM。」",
    key_concepts=["LLaMA-Factory", "QLoRA 训练配置", "学习率调度", "梯度累积", "Loss 监控"],
    platform_touches=["产出 NexusAgent 领域 LoRA 适配器", "对接平台 LLM 推理层"],
)

DAY_54 = DayPlan(
    day=54,
    title="模型评估与 LoRA 权重合并",
    phase=PHASE_5,
    epic=EPIC_E5,
    jira_stories=["NEXUS-507", "NEXUS-508"],
    morning=[
        "站会：分享训练 loss 曲线与遇到的问题",
        "理论：自动评估指标 ROUGE / BLEU / 困惑度",
        "人工评估方法论：幻觉率、相关性、安全性",
        "LoRA 合并 vs Adapter 热加载方案对比",
    ],
    afternoon=[
        "运行 run_eval.py 计算 ROUGE-L 分数",
        "执行 merge_lora.py 合并权重（dry_run + 实机）",
        "完成 eval_checklist.md 上线前检查",
        "20 条人工抽检并记录结果",
    ],
    evening=[
        "整理评估报告（自动 + 人工）",
        "决定是否需要增训或调参",
        "预习 Ollama / vLLM 推理部署",
    ],
    code_files=_day54_code(),
    homework_desc="对微调模型完成 20 条人工评估，填写 eval_checklist.md。运行 run_eval.py 并提交 JSON 结果。尝试 merge_lora（dry_run=False）。",
    homework_answer_hint="ROUGE-L > 0.35 为及格线。合并命令：llamafactory-cli export --finetuning_type lora。合并后模型约 14GB（7B fp16）。",
    architecture_mermaid="""flowchart TD
    LORA[LoRA Adapter] --> EVAL[自动评估 ROUGE]
    EVAL --> HUMAN[人工抽检]
    HUMAN --> PASS{通过?}
    PASS -->|是| MERGE[权重合并]
    PASS -->|否| RETRAIN[增训/调参]
    MERGE --> MERGED[合并模型]""",
    narration="林悦验收评估报告：「3 条样本出现幻觉，必须回炉重训。」陈工教合并技巧：「合并后单文件部署更简单，但失去多 adapter 切换灵活性。」",
    key_concepts=["ROUGE-L 评估", "人工抽检", "LoRA 权重合并", "幻觉检测", "上线检查清单"],
    platform_touches=["NexusAgent 微调模型质量门禁", "合并模型供 vLLM 加载"],
)

DAY_55 = DayPlan(
    day=55,
    title="Ollama 与 vLLM 本地推理服务",
    phase=PHASE_5,
    epic=EPIC_E5,
    jira_stories=["NEXUS-509", "NEXUS-510"],
    morning=[
        "站会：确认合并模型已就绪",
        "Ollama 架构与 Modelfile 语法",
        "vLLM 高性能推理原理：PagedAttention / 连续批处理",
        "OpenAI 兼容 API 标准与客户端对接",
    ],
    afternoon=[
        "编写 ollama_modelfile 并创建本地模型",
        "启动 start_vllm.sh 推理服务",
        "运行 client_demo.py 调用 API（mock + 实机）",
        "benchmark.py 压测延迟与吞吐",
    ],
    evening=[
        "对比 Ollama vs vLLM 延迟数据",
        "将 NexusAgent 平台 LLM 端点切换到本地 vLLM",
        "预习 Docker 容器化部署",
    ],
    code_files=_day55_code(),
    homework_desc="部署 vLLM 服务并用 client_demo.py 完成 5 轮对话测试。记录 P50/P99 延迟。编写 Ollama Modelfile 并 `ollama create`。",
    homework_answer_hint="vLLM 7B 在 4090 上 P50 约 80-150ms/token。client_demo 设 mock=False 连接实服务。Ollama 适合开发调试，vLLM 适合生产高并发。",
    architecture_mermaid="""flowchart LR
    MERGED[合并模型] --> OLLAMA[Ollama 本地]
    MERGED --> VLLM[vLLM 服务]
    VLLM --> API[OpenAI 兼容 API]
    API --> CLIENT[NexusAgent 客户端]""",
    narration="陈工：「API 按 token 计费，自部署 7B 微调模型每月省 80% 成本。vLLM 是生产标配，Ollama 是开发利器。」",
    key_concepts=["Ollama Modelfile", "vLLM 推理服务", "OpenAI 兼容 API", "PagedAttention", "推理性能基准"],
    platform_touches=["NexusAgent 接入本地 vLLM 推理端点", "替换 Day 39-50 的 API 调用为自部署模型"],
)

DAY_56 = DayPlan(
    day=56,
    title="Docker Compose 生产级部署",
    phase=PHASE_5,
    epic=EPIC_E5,
    jira_stories=["NEXUS-511", "NEXUS-512", "NEXUS-513"],
    morning=[
        "站会：确认 vLLM 服务稳定运行",
        "Docker 多阶段构建与镜像优化",
        "docker-compose.yml 服务编排讲解",
        "Nginx 反向代理与 SSE 流式配置",
    ],
    afternoon=[
        "编写并调试 docker-compose.yml 全栈编排",
        "构建 Dockerfile.api 应用镜像",
        "运行 deploy.sh 一键部署",
        "health_check.sh 全链路验证 + rollback.sh 演练",
    ],
    evening=[
        "完整部署截图：docker compose ps + 健康检查",
        "编写部署文档（环境变量、端口、依赖）",
        "预习安全合规要求",
    ],
    code_files=_day56_code(),
    homework_desc="使用 deploy/docker-compose.yml 完成全栈部署（API + vLLM + Postgres + Redis + Chroma + Nginx）。提交 deploy.sh 执行日志和健康检查截图。",
    homework_answer_hint="模型文件放 deploy/models/nexus-qwen-merged/。无 GPU 可注释 vLLM 服务，设 LLM_BASE_URL 为外部 API。健康检查 curl http://localhost/health 返回 200。",
    architecture_mermaid="""flowchart TB
    NGINX[Nginx :80] --> API[FastAPI :8080]
    API --> PG[(PostgreSQL)]
    API --> REDIS[(Redis)]
    API --> CHROMA[(Chroma)]
    API --> VLLM[vLLM :8000]
    API --> MINIO[(MinIO)]""",
    narration="运维老王加入站会：「生产环境不允许裸跑 Python 进程。今天交付的 docker-compose 要能在一台新机器上 10 分钟拉起全栈。」",
    key_concepts=["Docker Compose 编排", "多服务依赖管理", "Nginx 反向代理", "健康检查", "一键部署脚本"],
    platform_touches=["NexusAgent v0.5 生产部署架构落地", "完整平台容器化交付"],
)

DAY_57 = DayPlan(
    day=57,
    title="安全合规：审计日志与内容过滤",
    phase=PHASE_5,
    epic=EPIC_E5,
    jira_stories=["NEXUS-514", "NEXUS-515"],
    morning=[
        "站会：部署验收与问题复盘",
        "生成式 AI 合规法规要点（暂行办法）",
        "企业数据安全：PII 脱敏、审计日志、RBAC",
        "Prompt 注入攻击防护策略",
    ],
    afternoon=[
        "实现 audit_log.py 结构化审计日志",
        "开发 content_filter.py 输入输出过滤",
        "配置 rbac_policy.yaml 权限策略",
        "完成 compliance_checklist.md 自检",
    ],
    evening=[
        "将安全模块集成到 Day 56 部署栈",
        "Phase 5 阶段复盘与知识测验",
        "预习毕业设计选题要求",
    ],
    code_files=_day57_code(),
    homework_desc="实现审计日志 + 内容过滤并集成到 API 中间件。完成 compliance_checklist.md 全部勾选项。编写 3 条 Prompt 注入测试用例。",
    homework_answer_hint="AuditLogger 写入 JSONL 按日分割。ContentFilter 拦截「忽略指令」「DROP TABLE」等模式。RBAC 默认 deny，显式授权。",
    architecture_mermaid="""flowchart TD
    INPUT[用户输入] --> FILTER[内容过滤]
    FILTER -->|安全| LLM[模型推理]
    FILTER -->|拦截| REJECT[拒绝响应]
    LLM --> OUT_FILTER[输出过滤]
    OUT_FILTER --> AUDIT[审计日志]
    AUDIT --> RESPONSE[返回用户]""",
    narration="法务张姐讲解合规红线：「训练数据不能有真实客户信息，推理日志保留 180 天，内容过滤是上线硬性要求。」Phase 5 收官。",
    key_concepts=["审计日志", "PII 脱敏", "内容安全过滤", "Prompt 注入防护", "RBAC 权限策略"],
    platform_touches=["NexusAgent 安全合规层", "满足企业上线安全审计要求"],
)

DAY_58 = DayPlan(
    day=58,
    title="毕业设计选题与项目脚手架",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-601", "NEXUS-602"],
    morning=[
        "毕业典礼 Phase 5 回顾，宣布毕业设计正式启动",
        "选题指南：3 个推荐方向 + 自由选题规则",
        "评审标准：功能完整度、技术深度、演示效果、文档质量",
        "毕业设计脚手架结构讲解",
    ],
    afternoon=[
        "确定选题并填写 PROJECT_PROPOSAL.md",
        "初始化 nexus_capstone 项目脚手架",
        "运行 main.py 验证 /health 端点",
        "创建 GitLab 毕业设计仓库并首次提交",
    ],
    evening=[
        "完成选题书（项目名称、背景、功能、技术方案）",
        "与导师 1v1 选题确认（15 分钟）",
        "规划 Day 59-64 模块开发排期",
    ],
    code_files=_grad_scaffold_base(),
    homework_desc="提交完整的 PROJECT_PROPOSAL.md 选题书 + 可运行的脚手架（uvicorn 启动，/health 返回 200）。创建 GitLab 仓库并邀请导师。",
    homework_answer_hint="选题应聚焦一个垂直场景（如客服助手、文档问答、数据分析 Agent）。脚手架含 README、requirements.txt、app/main.py、docker-compose.dev.yml。",
    architecture_mermaid="""flowchart TD
    TOPIC[选题确认] --> SCAFFOLD[项目脚手架]
    SCAFFOLD --> REPO[GitLab 仓库]
    REPO --> PLAN[模块开发计划]
    PLAN --> DEV[Day 59-64 开发]""",
    narration="陈工：「70 天学了什么，毕业设计就是证明。不要贪大求全，一个场景做深做透。」林悦：「答辩时评委最关心：解决了什么真实问题，技术选型为什么合理。」",
    key_concepts=["毕业设计选题", "项目脚手架", "技术方案设计", "里程碑规划", "FastAPI 骨架"],
    platform_touches=["基于 NexusAgent 平台能力构建独立毕业项目", "综合运用 Phase 1-5 全部技能"],
)

DAY_59 = DayPlan(
    day=59,
    title="毕业设计开发：用户认证模块",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-603"],
    morning=[
        "站会：选题评审反馈与调整",
        "JWT 认证原理与 OAuth2 密码模式",
        "SQLAlchemy ORM 模型设计",
        "密码哈希最佳实践（bcrypt）",
    ],
    afternoon=[
        "实现 auth/models.py 用户模型",
        "开发 auth/service.py 注册/登录/JWT",
        "编写 auth/router.py API 端点",
        "Postman/curl 测试注册登录流程",
    ],
    evening=[
        "集成 auth router 到 main.py",
        "编写认证模块 README",
        "预习 RAG 知识库设计",
    ],
    code_files=_merge_grad(_grad_scaffold_base(), _grad_auth_module()),
    homework_desc="完成用户注册、登录、JWT 签发功能。至少 2 个 API 端点可调用。密码必须哈希存储，禁止明文。",
    homework_answer_hint="POST /api/v1/auth/register + /login。JWT payload 含 sub(user_id) 和 exp。生产环境 SECRET_KEY 从环境变量读取。",
    architecture_mermaid="""flowchart LR
    CLIENT[客户端] --> REGISTER[注册 API]
    CLIENT --> LOGIN[登录 API]
    LOGIN --> JWT[JWT Token]
    JWT --> PROTECTED[受保护 API]""",
    narration="Day 59 起进入毕业设计冲刺周。陈工：「认证是一切的入口，没有用户体系的项目不算企业级。」",
    key_concepts=["JWT 认证", "密码哈希", "用户注册登录", "SQLAlchemy 模型", "API 路由设计"],
    platform_touches=["毕业项目用户体系", "对齐 NexusAgent 平台认证模块"],
)

DAY_60 = DayPlan(
    day=60,
    title="毕业设计开发：RAG 知识库模块",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-604"],
    morning=[
        "站会：认证模块进度检查",
        "文档分块策略：固定窗口 vs 语义分块",
        "混合检索：向量 + BM25 融合",
        "Chroma 集合管理与持久化",
    ],
    afternoon=[
        "实现 rag/ingest.py 文档入库",
        "开发 rag/retriever.py 混合检索",
        "编写 rag/router.py 上传与搜索 API",
        "上传 3 份领域文档并测试检索",
    ],
    evening=[
        "优化分块参数（chunk_size / overlap）",
        "记录检索准确率抽检结果",
        "预习 LangGraph Agent 编排",
    ],
    code_files=_merge_grad(_grad_scaffold_base(), _grad_auth_module(), _grad_rag_module()),
    homework_desc="实现文档上传 + 知识检索 API。上传至少 3 份文档，测试 10 个查询并记录 Top-3 命中率。",
    homework_answer_hint="chunk_size=500, overlap=50 为起点。HybridRetriever 融合向量分 + 关键词分。GET /api/v1/knowledge/search?q=...",
    architecture_mermaid="""flowchart TD
    DOC[文档上传] --> CHUNK[文本分块]
    CHUNK --> EMBED[向量化]
    EMBED --> CHROMA[(Chroma)]
    QUERY[用户查询] --> RETRIEVE[混合检索]
    CHROMA --> RETRIEVE
    RETRIEVE --> RESULTS[Top-K 结果]""",
    narration="林悦提供脱敏产品文档包。陈工：「RAG 是毕业设计的灵魂——没有知识库的 Agent 就是聊天机器人。」",
    key_concepts=["文档分块", "向量检索", "混合检索", "Chroma 集成", "知识库 API"],
    platform_touches=["毕业项目知识库层", "复用 NexusAgent RAG 架构"],
)

DAY_61 = DayPlan(
    day=61,
    title="毕业设计开发：Agent 编排模块",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-605"],
    morning=[
        "站会：RAG 检索效果评审",
        "LangGraph 状态机与 ReAct 模式回顾",
        "工具函数设计与 Agent 决策流程",
        "检索增强生成（RAG + Agent）架构",
    ],
    afternoon=[
        "实现 agent/graph.py 状态机与工具调用",
        "开发 agent/router.py 对话 API",
        "联通 RAG 检索工具到 Agent 流程",
        "测试 5 个多步推理场景",
    ],
    evening=[
        "优化 Agent 回答模板与拒答策略",
        "记录 Agent 链路日志",
        "预习 API 集成与中间件",
    ],
    code_files=_merge_grad(_grad_scaffold_base(), _grad_auth_module(), _grad_rag_module(), _grad_agent_module()),
    homework_desc="实现 Agent 对话 API，至少支持检索增强回答。测试 5 个场景：3 个知识库可回答 + 2 个应拒答/转人工。",
    homework_answer_hint="run_agent 先判断是否需要检索，调用 search_tool，再合成回答。超范围问题返回「建议联系人工支持」。",
    architecture_mermaid="""flowchart TD
    USER[用户问题] --> AGENT[Agent 状态机]
    AGENT --> DECIDE{需要检索?}
    DECIDE -->|是| TOOL[search_tool]
    TOOL --> RAG[RAG 检索]
    RAG --> SYNTH[合成回答]
    DECIDE -->|否| SYNTH
    SYNTH --> ANSWER[返回用户]""",
    narration="陈工演示 LangGraph 调试：「Agent 的价值不是聊天，是能自主决定调用什么工具、什么时候该说不。」",
    key_concepts=["LangGraph 状态机", "ReAct 模式", "工具调用", "RAG 增强 Agent", "拒答策略"],
    platform_touches=["毕业项目 Agent 引擎", "NexusAgent 多 Agent 编排简化版"],
)

DAY_62 = DayPlan(
    day=62,
    title="毕业设计开发：API 集成与网关",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-606"],
    morning=[
        "站会：Agent 模块联调问题排查",
        "中间件设计：日志、限流、鉴权、CORS",
        "API 版本管理与 OpenAPI 文档",
        "模块聚合与服务发现模式",
    ],
    afternoon=[
        "实现 api/middleware.py 日志与限流",
        "开发 api/router.py 状态聚合端点",
        "编写 main_integrated.py 注册全部路由",
        "Swagger UI 验证 API 文档完整性",
    ],
    evening=[
        "全模块联调：注册 → 上传文档 → Agent 对话",
        "修复集成 bug 并记录",
        "预习前端界面开发",
    ],
    code_files=_merge_grad(
        _grad_scaffold_base(), _grad_auth_module(), _grad_rag_module(),
        _grad_agent_module(), _grad_api_module(),
    ),
    homework_desc="完成全模块集成（main_integrated.py），所有 API 在 Swagger 可见。完成端到端联调并截图。",
    homework_answer_hint="app.include_router 注册 auth/rag/agent/api 四个路由。RequestLogMiddleware 打印请求耗时。RateLimitMiddleware 限 100 req/min/IP。",
    architecture_mermaid="""flowchart TB
    NGINX[API 网关] --> MW[中间件链]
    MW --> AUTH[认证模块]
    MW --> RAG[知识库模块]
    MW --> AGENT[Agent 模块]
    MW --> STATUS[状态 API]""",
    narration="陈工：「单个模块能跑不算数，集成后接口对齐、错误传播、日志统一才是工程能力。」",
    key_concepts=["API 集成", "中间件链", "请求日志", "限流策略", "OpenAPI 文档"],
    platform_touches=["毕业项目 API 层统一入口", "NexusAgent 网关模式"],
)

DAY_63 = DayPlan(
    day=63,
    title="毕业设计开发：前端界面",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-607"],
    morning=[
        "站会：API 联调结果评审",
        "轻量前端方案：纯 HTML/JS vs Vue/React",
        "聊天 UI 设计模式：消息气泡、流式输出、加载态",
        "静态文件挂载与 CORS 配置",
    ],
    afternoon=[
        "编写 frontend/index.html 聊天界面",
        "实现 static_mount.py 挂载前端",
        "对接 /api/v1/agent/chat 端点",
        "UI 美化与移动端适配",
    ],
    evening=[
        "录制 2 分钟功能演示视频",
        "收集同学试用反馈并改进",
        "预习测试与性能优化",
    ],
    code_files=_merge_grad(
        _grad_scaffold_base(), _grad_auth_module(), _grad_rag_module(),
        _grad_agent_module(), _grad_api_module(), _grad_frontend_module(),
    ),
    homework_desc="完成可交互的聊天前端界面，能发送消息并显示 Agent 回复。提交界面截图和演示视频链接。",
    homework_answer_hint="fetch POST /api/v1/agent/chat，渲染用户/机器人消息气泡。StaticFiles 挂载 frontend/ 到根路径。",
    architecture_mermaid="""flowchart LR
    BROWSER[浏览器] --> HTML[聊天界面]
    HTML --> FETCH[fetch API]
    FETCH --> AGENT_API[Agent Chat API]
    AGENT_API --> HTML""",
    narration="林悦：「评委第一眼看到的就是界面。不求华丽，但要清晰、流畅、无 bug。」",
    key_concepts=["聊天 UI 设计", "Fetch API 调用", "静态文件挂载", "用户体验", "演示视频录制"],
    platform_touches=["毕业项目用户界面", "NexusAgent Web 控制台简化版"],
)

DAY_64 = DayPlan(
    day=64,
    title="毕业设计开发：测试与性能优化",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-608"],
    morning=[
        "站会：前端演示评审",
        "pytest 单元测试最佳实践",
        "API 压测工具：hey / locust / k6",
        "性能优化清单：缓存、连接池、异步 IO",
    ],
    afternoon=[
        "编写 tests/test_auth.py / test_rag.py / test_agent.py",
        "运行 pytest 确保全部通过",
        "执行 benchmark.sh 压测 /health 端点",
        "修复测试发现的 bug 并优化",
    ],
    evening=[
        "测试覆盖率报告截图",
        "整理已知问题清单与后续优化计划",
        "开始准备答辩 PPT 大纲",
    ],
    code_files=_merge_grad(
        _grad_scaffold_base(), _grad_auth_module(), _grad_rag_module(),
        _grad_agent_module(), _grad_api_module(), _grad_frontend_module(),
        _grad_test_module(),
    ),
    homework_desc="编写并通过全部单元测试（pytest）。完成压测报告（100 请求，10 并发）。修复至少 2 个测试发现的 bug。",
    homework_answer_hint="pytest tests/ -v 全部 PASS。压测 hey -n 100 -c 10。常见 bug：JWT 过期未处理、空文档上传未校验。",
    architecture_mermaid="""flowchart TD
    CODE[项目代码] --> UNIT[单元测试 pytest]
    CODE --> BENCH[压测 benchmark]
    UNIT --> FIX[修复 Bug]
    BENCH --> OPT[性能优化]
    FIX --> RELEASE[发布候选]
    OPT --> RELEASE""",
    narration="陈工：「没有测试的项目不能上线。今天把质量门禁建好，答辩时才有底气。」",
    key_concepts=["pytest 单元测试", "API 压测", "Bug 修复", "性能优化", "测试覆盖率"],
    platform_touches=["毕业项目质量保障", "NexusAgent CI/CD 测试规范"],
)

DAY_65 = DayPlan(
    day=65,
    title="毕业答辩：项目演示与评审",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-609"],
    morning=[
        "答辩流程说明：10 分钟演示 + 5 分钟 Q&A",
        "PPT 结构指导：背景 → 方案 → 演示 → 总结",
        "演示环境检查清单（网络、GPU、备用录屏）",
        "第一批学员答辩（上午场）",
    ],
    afternoon=[
        "第二批学员答辩（下午场）",
        "评委点评与改进建议记录",
        "互评环节：每组点评另一组项目",
        "答辩成绩统计与反馈",
    ],
    evening=[
        "根据答辩反馈列出改进项",
        "整理答辩 PPT 最终版",
        "预习简历编写要点",
    ],
    code_files={
        f"{GRAD_PROJECT_ROOT}/docs/DEFENSE_GUIDE.md": '''# 毕业答辩指南

## 答辩流程（15 分钟/人）
1. **项目介绍**（3 分钟）：背景、目标、技术栈
2. **架构讲解**（2 分钟）：模块划分、数据流
3. **Live Demo**（5 分钟）：注册 → 上传文档 → Agent 对话
4. **Q&A**（5 分钟）：评委提问

## 评分标准（满分 100）
| 维度 | 分值 | 说明 |
|------|------|------|
| 功能完整 | 30 | 核心流程可跑通 |
| 技术深度 | 25 | 架构合理、代码规范 |
| 演示效果 | 20 | 流畅、无重大 bug |
| 文档质量 | 15 | README、API 文档齐全 |
| 答辩表现 | 10 | 表达清晰、回答问题 |

## 演示检查清单
- [ ] 服务已启动，/health 正常
- [ ] 测试账号已注册
- [ ] 知识库文档已上传
- [ ] 3 个演示问题已准备
- [ ] 备用录屏视频已就绪
''',
        f"{GRAD_PROJECT_ROOT}/docs/DEFENSE_TEMPLATE.pptx.md": '''# 答辩 PPT 大纲（Markdown 版）

## Slide 1: 封面
- 项目名称、学员姓名、日期

## Slide 2: 问题背景
- 企业痛点（1-2 句话）

## Slide 3: 解决方案
- 核心功能架构图

## Slide 4: 技术栈
- FastAPI / Chroma / LangGraph / Docker

## Slide 5-7: 模块演示
- 认证 / RAG / Agent 各一页截图

## Slide 8: Live Demo
- 演示脚本（逐步操作）

## Slide 9: 成果与数据
- 测试通过率、压测数据、检索准确率

## Slide 10: 总结与展望
- 收获、不足、后续计划
''',
    },
    homework_desc="完成毕业答辩（演示 + Q&A）。提交答辩 PPT 和演示录屏。根据评委反馈列出 3 条改进项。",
    homework_answer_hint="Demo 脚本：注册账号 → 上传 FAQ 文档 → 提问「如何重置密码」→ 展示 Agent 检索增强回答。PPT 控制在 10 页以内。",
    architecture_mermaid="""flowchart LR
    PPT[答辩 PPT] --> DEMO[Live Demo]
    DEMO --> QA[Q&A 环节]
    QA --> SCORE[评分反馈]
    SCORE --> IMPROVE[改进计划]""",
    narration="答辩日。林悦主持：「70 天的学习，15 分钟来证明。放松，你们比想象中准备得更充分。」",
    key_concepts=["毕业答辩", "项目演示", "技术评审", "PPT 制作", "Q&A 应对"],
    platform_touches=["毕业设计最终交付验收", "NexusAgent 训练营结业考核"],
)

DAY_66 = DayPlan(
    day=66,
    title="求职简历：AI 工程师简历打造",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-610"],
    morning=[
        "AI 工程师简历结构与关键词优化",
        "项目经历描述公式：STAR 法则",
        "70 天训练营项目如何写进简历",
        "简历常见误区：堆砌技术栈、缺乏量化",
    ],
    afternoon=[
        "编写个人技术简历（中文版）",
        "将毕业设计包装为「企业级项目经历」",
        "GitHub 主页优化：Pinned Repos + README",
        "同学互审简历并给出修改建议",
    ],
    evening=[
        "提交简历终稿（PDF）",
        "注册 Boss直聘/拉勾/LinkedIn",
        "预习技术面试高频题",
    ],
    code_files={
        "career/resume_template.md": '''# AI 应用开发工程师 — 简历模板

## 个人信息
- 姓名 | 电话 | 邮箱 | GitHub

## 技术栈
Python · FastAPI · LangChain/LangGraph · RAG · Docker · PostgreSQL · Redis · Chroma

## 项目经历

### Nexus Capstone — 企业级 AI Agent 平台（毕业设计）
**时间**：2026.XX - 2026.XX | **角色**：独立开发者
- 基于 FastAPI + LangGraph 构建多模块 AI Agent 平台，支持用户认证、RAG 知识库问答、Agent 工具编排
- 实现混合检索（向量 + 关键词），文档检索 Top-3 命中率达 XX%
- 使用 QLoRA 微调 7B 领域模型，客服问答 ROUGE-L 提升 XX%
- Docker Compose 一键部署全栈（API + vLLM + Chroma + PostgreSQL），P99 延迟 < XXms
- **技术栈**：Python, FastAPI, LangGraph, Chroma, Docker, vLLM, LLaMA-Factory

### NexusAgent 训练营项目（70 天）
- 完成 70 天全栈 AI 工程训练，累计代码 XX 行，涵盖 CLI/API/RAG/Agent/微调/部署
- GitLab 提交 XX 次 MR，通过 Code Review XX 次

## 教育背景
（填写）

## 自我评价
（2-3 句话，突出 AI 工程能力 + 学习能力）
''',
        "career/github_profile_README.md": '''# Hi, I'm [Your Name] 👋

## 🚀 AI Application Engineer
Graduate of NexusAgent 70-Day Bootcamp | Building enterprise AI agents

## 🛠 Tech Stack
`Python` `FastAPI` `LangGraph` `RAG` `Docker` `vLLM` `Chroma`

## 📌 Featured Projects
- **[nexus-capstone](link)** — Enterprise AI Agent platform with RAG + fine-tuning
- **[nexus-agent-bootcamp](link)** — 70-day AI engineering bootcamp coursework

## 📊 Bootcamp Stats
- 70 days | XX commits | XX lines of code
- Skills: CLI → API → RAG → Multi-Agent → Fine-tuning → Production Deploy
''',
        "career/resume_checklist.md": '''# 简历自检清单
- [ ] 一页纸原则（应届生）
- [ ] 每个项目有量化数据（命中率、延迟、代码量）
- [ ] 技术栈与 JD 关键词对齐
- [ ] 无错别字，格式统一
- [ ] GitHub 链接可访问，有代表性项目
- [ ] 毕业设计已写入项目经历
''',
    },
    homework_desc="完成中文技术简历（PDF）和 GitHub Profile README。至少包含毕业设计和训练营两个项目经历，每个项目 3-4 条量化描述。",
    homework_answer_hint="用 STAR 法则：「基于 FastAPI 构建 Agent 平台（S），解决客服重复问答痛点（T），实现 RAG+微调（A），检索命中率 85%（R）。」",
    architecture_mermaid="""flowchart TD
    PROJECT[毕业设计] --> RESUME[简历项目经历]
    BOOTCAMP[70天训练营] --> RESUME
    RESUME --> GITHUB[GitHub 主页]
    GITHUB --> APPLY[投递简历]""",
    narration="HR 刘姐分享：「AI 岗位简历筛选 30 秒一份。项目经历比学历重要，量化数据比形容词重要。」",
    key_concepts=["简历撰写", "STAR 法则", "项目经历包装", "GitHub 优化", "关键词匹配"],
    platform_touches=["将 NexusAgent 训练营成果转化为求职竞争力"],
)

DAY_67 = DayPlan(
    day=67,
    title="技术面试（一）：Python 与后端基础",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-611"],
    morning=[
        "技术面试流程与考察维度",
        "Python 高频题：装饰器、生成器、GIL、异步",
        "FastAPI 面试题：依赖注入、中间件、生命周期",
        "数据库面试题：索引、事务、连接池",
    ],
    afternoon=[
        "模拟面试 Round 1：Python 基础（1v1）",
        "模拟面试 Round 2：后端 API 设计",
        "面试复盘：错题本记录",
        "手写代码练习：LRU Cache / 线程安全单例",
    ],
    evening=[
        "整理 Python 面试题笔记（20 题）",
        "完成 3 道 LeetCode Easy",
        "预习 RAG/LLM 面试题",
    ],
    code_files={
        "interview/day67_python_basics.py": '''#!/usr/bin/env python3
"""
Day 67 — Python 面试高频题跟敲
"""
from functools import wraps
from collections import OrderedDict


# --- 1. 装饰器：计时 + 日志 ---
def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {(time.perf_counter()-start)*1000:.1f}ms")
        return result
    return wrapper


# --- 2. 生成器：内存友好的大数据处理 ---
def read_large_file(path: str):
    with open(path) as f:
        for line in f:
            yield line.strip()


# --- 3. LRU Cache 实现（面试手写题）---
class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# --- 4. 异步 FastAPI 依赖注入示例 ---
@timed
def demo_lru():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    print(cache.get(1))
    cache.put(3, "c")
    print(cache.get(2))  # -1


if __name__ == "__main__":
    demo_lru()
''',
        "interview/day67_questions.md": '''# Day 67 面试题清单

## Python 基础
1. 解释 GIL 及其对多线程的影响
2. 装饰器原理与 @wraps 作用
3. 生成器 vs 迭代器 vs 协程
4. *args 和 **kwargs 使用场景
5. 深拷贝 vs 浅拷贝

## FastAPI / 后端
6. 依赖注入 DI 的优势
7. 中间件执行顺序
8. RESTful API 设计原则
9. JWT 认证流程
10. 数据库连接池为什么必要

## 手写代码
11. 实现 LRU Cache
12. 单例模式（线程安全）
13. 反转链表
''',
    },
    homework_desc="完成模拟面试复盘笔记，整理 20 道 Python/后端面试题答案。手写实现 LRUCache 并通过基本测试。",
    homework_answer_hint="GIL：同一时刻只有一个线程执行 Python 字节码，CPU 密集型用多进程，IO 密集型用多线程/异步。LRU 用 OrderedDict move_to_end + popitem。",
    architecture_mermaid="""flowchart LR
    PREP[面试准备] --> MOCK[模拟面试]
    MOCK --> REVIEW[复盘错题]
    REVIEW --> NOTES[面试笔记]
    NOTES --> NEXT[Day 68 RAG/LLM]""",
    narration="陈工扮演面试官：「不要背答案，要说清楚原理和你的实践经验。训练营的项目就是最好的素材。」",
    key_concepts=["Python 面试题", "装饰器与生成器", "LRU Cache", "FastAPI 原理", "模拟面试"],
    platform_touches=["NexusAgent 技术栈面试准备"],
)

DAY_68 = DayPlan(
    day=68,
    title="技术面试（二）：RAG 与 LLM 应用",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-612"],
    morning=[
        "RAG 面试题：分块、检索、重排序、评估",
        "LLM 面试题：Prompt Engineering、微调、推理优化",
        "Agent 面试题：ReAct、工具调用、状态管理",
        "系统设计题：设计一个客服 AI 系统",
    ],
    afternoon=[
        "模拟面试 Round 3：RAG 架构设计",
        "模拟面试 Round 4：LLM 微调与部署",
        "白板设计：从 0 设计企业知识库问答系统",
        "面试复盘与答案优化",
    ],
    evening=[
        "整理 RAG/LLM 面试题笔记（20 题）",
        "绘制系统设计图（Mermaid）",
        "预习行为面试与项目深挖",
    ],
    code_files={
        "interview/day68_rag_design.md": '''# 系统设计题：企业知识库问答系统

## 需求
- 500 员工，10 万篇内部文档
- 支持多轮对话 + 引用溯源
- P99 延迟 < 3s，可用性 99.9%

## 架构方案
```mermaid
flowchart TB
    USER[用户] --> GW[API Gateway]
    GW --> CHAT[对话服务]
    CHAT --> AGENT[Agent 编排]
    AGENT --> RAG[RAG 检索]
    RAG --> CHROMA[(Chroma)]
    AGENT --> LLM[vLLM 微调模型]
    CHAT --> REDIS[(Redis 会话)]
```

## 关键设计决策
1. **分块**：512 token + 50 overlap，语义分块优化
2. **检索**：混合检索（向量 0.7 + BM25 0.3）+ Reranker
3. **微调**：QLoRA rank=8，3000 条领域 QA
4. **部署**：Docker Compose，vLLM + FastAPI
5. **评估**：ROUGE-L + 人工抽检 + 在线 A/B

## 扩展讨论
- 如何处理文档更新？→ 增量索引 + 版本管理
- 如何防止幻觉？→ 引用强制 + 置信度阈值
- 如何控制成本？→ 缓存热门查询 + 小模型路由
''',
        "interview/day68_llm_questions.md": '''# Day 68 RAG/LLM 面试题

## RAG
1. 文档分块策略有哪些？各优缺点？
2. 混合检索如何融合向量分和 BM25 分？
3. 如何评估 RAG 系统质量？
4. Embedding 模型如何选择？
5. 如何处理多模态文档（PDF/表格）？

## LLM / 微调
6. LoRA 原理？rank 如何选择？
7. QLoRA vs LoRA 区别？
8. 如何减少 LLM 幻觉？
9. vLLM 为什么比原生推理快？
10. Prompt Engineering 最佳实践？

## Agent
11. ReAct 模式是什么？
12. LangGraph 状态机优势？
13. 工具调用失败如何处理？
14. 多 Agent 协作模式？
15. MCP 协议是什么？
''',
        "interview/day68_whiteboard.py": '''#!/usr/bin/env python3
"""Day 68 — 白板编程：简化版 RAG Pipeline（面试手写）"""

def rag_pipeline(query: str, documents: list[str], top_k: int = 3) -> str:
    """面试白板版 RAG：关键词匹配 + 模板回答"""
    # Step 1: 检索（简化为关键词匹配）
    scored = []
    for doc in documents:
        score = sum(1 for word in query.split() if word in doc)
        scored.append((score, doc))
    scored.sort(reverse=True)
    top_docs = [doc for _, doc in scored[:top_k]]

    # Step 2: 组装上下文
    context = "\\n".join(top_docs) if top_docs else "无相关文档"

    # Step 3: 生成回答（生产环境调用 LLM）
    return f"根据知识库资料：\\n{context}\\n\\n以上信息供参考。"


if __name__ == "__main__":
    docs = ["重置密码请进入管理后台", "RAG 需要 Chroma 在线", "API 限流默认 100/min"]
    print(rag_pipeline("如何重置密码", docs))
''',
    },
    homework_desc="完成系统设计白板图（企业知识库问答）并口头讲解 10 分钟。整理 15 道 RAG/LLM 面试题答案。",
    homework_answer_hint="系统设计分五层：接入层 → 应用层 → Agent 层 → 数据层 → 模型层。RAG 核心：分块 → 嵌入 → 检索 → 重排 → 生成。",
    architecture_mermaid="""flowchart TB
    INTERVIEW[模拟面试] --> RAG_Q[RAG 题目]
    INTERVIEW --> LLM_Q[LLM 题目]
    INTERVIEW --> DESIGN[系统设计]
    DESIGN --> WHITEBOARD[白板架构图]""",
    narration="大厂面试官视频连线：「我们不考 LeetCode Hard，考你能不能设计一个能上线的 RAG 系统。」",
    key_concepts=["RAG 系统设计", "LLM 面试题", "混合检索", "白板编程", "架构设计"],
    platform_touches=["基于 NexusAgent 项目经验应对 RAG/LLM 面试"],
)

DAY_69 = DayPlan(
    day=69,
    title="技术面试（三）：项目深挖与行为面试",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-613"],
    morning=[
        "项目深挖技巧：面试官想听什么",
        "行为面试 STAR 法则实战",
        "常见行为题：冲突、失败、领导力",
        "薪资谈判基础与 Offer 比较",
    ],
    afternoon=[
        "模拟面试 Round 5：毕业设计深挖（30 分钟）",
        "模拟面试 Round 6：行为面试",
        "交叉互评：每组 2 人互相当面试官",
        "个人面试弱点分析与改进计划",
    ],
    evening=[
        "准备 5 个行为面试故事（STAR 格式）",
        "完善毕业设计 README 作为面试作品",
        "预习结业典礼流程",
    ],
    code_files={
        "interview/day69_star_stories.md": '''# 行为面试 STAR 故事库

## 故事 1：解决技术难题
- **S**：毕业设计 RAG 检索命中率仅 60%
- **T**：需要将命中率提升到 80% 以上
- **A**：分析 bad case，调整分块策略（500→300），引入混合检索，扩充训练数据
- **R**：命中率提升至 85%，答辩获优秀

## 故事 2：团队协作
- **S**：训练营小组项目中 API 接口定义不一致
- **T**：需要统一接口规范保证联调进度
- **A**：主动编写 OpenAPI 文档，组织接口评审会，推动统一错误码
- **R**：联调时间从 3 天缩短到 1 天

## 故事 3：快速学习
- **S**：Day 51 前从未接触模型微调
- **T**：一周内完成 QLoRA 微调并部署
- **A**：系统学习 LLaMA-Factory 文档，在云 GPU 反复实验，记录每次实验参数
- **R**：成功微调客服模型，ROUGE-L 0.42

## 故事 4：处理失败
- **S**：首次 Docker 部署健康检查一直超时
- **T**：需要在答辩前完成部署
- **A**：逐服务排查日志，发现 Postgres 未就绪就启动 API，添加 depends_on + healthcheck
- **R**：部署成功，编写 deploy.sh 自动化脚本

## 故事 5：主动性
- **S**：课程未要求内容安全模块
- **T**：企业上线必须有审计和过滤
- **A**：自学合规要求，实现 AuditLogger + ContentFilter 并集成
- **R**：项目安全合规性获评委好评
''',
        "interview/day69_project_deep_dive.md": '''# 毕业设计面试深挖准备

## 必问题目与回答要点

### Q: 为什么选择这个技术栈？
A: FastAPI（异步高性能）+ Chroma（轻量向量库）+ LangGraph（状态机 Agent）+ Docker（生产部署），平衡学习成本与企业需求。

### Q: 最大技术挑战是什么？
A: RAG 检索准确率。通过混合检索 + 分块优化 + 微调模型三管齐下解决。

### Q: 如果用户量增长 10 倍怎么办？
A: API 水平扩展 + Redis 会话共享 + Chroma 分片 + vLLM 多实例负载均衡 + CDN 静态资源。

### Q: 如何保证回答不幻觉？
A: 强制引用检索结果 + 置信度阈值拒答 + 微调减少领域幻觉 + 人工审核高频问题。

### Q: 项目下一步计划？
A: 多模态文档支持、用户反馈闭环微调、A/B 测试框架、K8s 部署。
''',
        "interview/day69_salary_guide.md": '''# 薪资谈判指南（AI 应用开发初级岗）

## 市场行情参考（2026）
- 初级 AI 应用工程师：15-25K（一线城市）
- 有完整项目经验：20-30K
- 训练营 + 毕业设计优秀：可争取区间上限

## 谈判技巧
1. 了解市场价位，给出区间而非单点
2. 用项目量化数据支撑要价
3. 综合考虑：薪资 + 成长空间 + 技术栈匹配度
4. 拿到 Offer 再谈，多 Offer 博弈

## 红线
- 不要贬低前雇主/同学
- 不要虚报项目经验
- 不要只谈钱不谈成长
''',
    },
    homework_desc="准备 5 个 STAR 行为面试故事。完成 30 分钟毕业设计深挖模拟面试。整理项目深挖 10 题答案。",
    homework_answer_hint="项目深挖核心：为什么这样设计 → 遇到什么困难 → 怎么解决的 → 效果如何（量化）。行为面试用 STAR，每个故事 2 分钟。",
    architecture_mermaid="""flowchart TD
    PROJECT[毕业设计] --> DEEP[深挖准备]
    EXPERIENCE[训练营经历] --> STAR[STAR 故事]
    DEEP --> MOCK[模拟面试]
    STAR --> MOCK
    MOCK --> OFFER[求职就绪]""",
    narration="最后一天模拟面试。陈工：「技术过了只是门槛，项目深挖和行为面试决定 Offer 质量。」",
    key_concepts=["项目深挖", "STAR 行为面试", "薪资谈判", "面试复盘", "求职准备"],
    platform_touches=["NexusAgent 训练营完整项目经验面试转化"],
)

DAY_70 = DayPlan(
    day=70,
    title="结业典礼：70 天旅程回顾与展望",
    phase=PHASE_6,
    epic=EPIC_E6,
    jira_stories=["NEXUS-614"],
    morning=[
        "70 天学习旅程回顾视频",
        "优秀学员项目展示（Top 3）",
        "结业证书颁发仪式",
        "陈工结业寄语与行业展望",
    ],
    afternoon=[
        "学员成长分享环节",
        "企业合作方招聘宣讲",
        "校友网络建立（微信群 + GitHub Org）",
        "合影留念与自由交流",
    ],
    evening=[
        "填写训练营反馈问卷",
        "更新个人简历投递第一批岗位",
        "撰写个人技术博客：70 天总结",
        "开启下一阶段学习规划",
    ],
    code_files={
        "graduation/CERTIFICATE.md": '''# 🎓 NexusAgent 训练营结业证书

## 兹证明

**[学员姓名]**

已完成智链科技 NexusAgent **70 天 AI 应用开发训练营**全部课程，

掌握从 Python 基础到企业级 AI Agent 平台开发的完整技能链：

| 阶段 | 天数 | 核心能力 | 状态 |
|------|------|---------|------|
| Phase 1 | Day 1-14 | Python 基础与 CLI | ✅ |
| Phase 2 | Day 15-24 | API 与 Web 层 | ✅ |
| Phase 3 | Day 25-38 | RAG 知识库 | ✅ |
| Phase 4 | Day 39-50 | 多 Agent 编排 | ✅ |
| Phase 5 | Day 51-57 | 微调与部署 | ✅ |
| Phase 6 | Day 58-70 | 毕业设计 | ✅ |

**累计代码量**：约 98,000 行  
**毕业设计评级**：[优秀/良好/合格]  
**颁发日期**：2026 年 XX 月 XX 日

---
智链科技培训中心 | Tech Lead: 陈工 | 产品经理: 林悦
''',
        "graduation/70day_summary_blog.md": '''# 我的 70 天 AI 工程之旅

## 开篇
（为什么选择这个训练营，初始水平）

## Phase 1-2：从 Hello World 到 API（Day 1-24）
（关键收获、代表项目）

## Phase 3-4：RAG 与 Agent（Day 25-50）
（技术突破、踩坑记录）

## Phase 5：微调与部署（Day 51-57）
（微调成果、Docker 部署经验）

## Phase 6：毕业设计（Day 58-70）
（项目介绍、答辩心得）

## 技能图谱
```mermaid
mindmap
  root((AI 工程师))
    Python
      FastAPI
      异步编程
    LLM
      Prompt Engineering
      微调 QLoRA
      vLLM 部署
    RAG
      向量检索
      混合检索
    Agent
      LangGraph
      工具调用
    DevOps
      Docker
      CI/CD
```

## 下一步计划
（求职目标、持续学习方向）

## 致谢
（导师、同学、家人）
''',
        "graduation/next_steps.md": '''# 结业后学习路线图

## 短期（1-3 个月）
- [ ] 投递 AI 应用开发岗位，目标 10+ 面试
- [ ] 完善毕业设计（根据答辩反馈）
- [ ] 考取云厂商 AI 认证（阿里云/华为云）

## 中期（3-6 个月）
- [ ] 深入学习 LLM 推理优化（TensorRT-LLM / TGI）
- [ ] 贡献开源项目（LangChain / LLaMA-Factory）
- [ ] 写 3 篇技术博客建立个人品牌

## 长期（6-12 个月）
- [ ] 独立负责企业 AI 项目
- [ ] 掌握 K8s + GPU 调度
- [ ] 探索 Agent 前沿（Multi-Agent / Computer Use）

## 推荐资源
- 书籍：《Designing Machine Learning Systems》
- 课程：DeepLearning.AI LangChain 系列
- 社区：Hugging Face / LangChain Discord
- 校友群：NexusAgent Graduates 2026
''',
        "graduation/feedback_survey.json": '''{
  "survey_title": "NexusAgent 70天训练营结业反馈",
  "questions": [
    {"id": 1, "question": "整体满意度（1-10）", "type": "rating"},
    {"id": 2, "question": "最有价值的模块", "type": "multi_choice", "options": ["Python基础", "RAG", "Agent", "微调", "毕业设计"]},
    {"id": 3, "question": "需要改进的地方", "type": "text"},
    {"id": 4, "question": "是否愿意推荐给朋友", "type": "rating", "scale": "NPS"},
    {"id": 5, "question": "结业后最想做的工作", "type": "text"}
  ]
}''',
    },
    homework_desc="撰写 70 天学习总结博客（1000 字以上）。填写结业反馈问卷。更新简历并投递至少 3 个岗位。",
    homework_answer_hint="博客按 Phase 分段，每段含具体项目和技术收获。反馈问卷诚实填写助力下期改进。投递优先 AI 应用开发 / LLM 工程师岗位。",
    architecture_mermaid="""flowchart TD
    START[Day 1 入门] --> P1[Phase 1-2 基础]
    P1 --> P2[Phase 3-4 RAG/Agent]
    P2 --> P3[Phase 5 微调部署]
    P3 --> P4[Phase 6 毕业设计]
    P4 --> GRAD[Day 70 结业]
    GRAD --> CAREER[职业发展]""",
    narration="结业典礼。陈工：「70 天前你们连 f-string 都不会，今天能独立部署一个企业级 AI Agent 平台。这不是终点，是你们 AI 工程师职业生涯的起点。」全场掌声。",
    key_concepts=["70 天学习回顾", "结业证书", "职业发展", "校友网络", "持续学习"],
    platform_touches=["NexusAgent 训练营圆满结业", "从学员到 AI 应用开发工程师"],
)

# ---------------------------------------------------------------------------
# 导出
# ---------------------------------------------------------------------------

DAYS_51_TO_70: list[DayPlan] = [
    DAY_51, DAY_52, DAY_53, DAY_54, DAY_55, DAY_56, DAY_57,
    DAY_58, DAY_59, DAY_60, DAY_61, DAY_62, DAY_63, DAY_64,
    DAY_65, DAY_66, DAY_67, DAY_68, DAY_69, DAY_70,
]

