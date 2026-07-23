#!/bin/bash
set -euo pipefail
MODEL_PATH="${MODEL_PATH:-./output/nexus-qwen-merged}"
python -m vllm.entrypoints.openai.api_server \
  --model "$MODEL_PATH" --host 0.0.0.0 --port 8000 \
  --served-model-name nexus-agent
