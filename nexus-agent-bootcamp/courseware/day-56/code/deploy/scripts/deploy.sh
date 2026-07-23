#!/bin/bash
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
