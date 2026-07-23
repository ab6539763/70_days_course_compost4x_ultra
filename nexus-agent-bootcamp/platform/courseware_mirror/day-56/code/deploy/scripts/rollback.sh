#!/bin/bash
cd "$(dirname "$0")/.."
docker compose down
echo "回滚完成"
