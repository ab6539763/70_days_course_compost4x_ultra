#!/bin/bash
# Day 64 — 性能基准测试
echo "=== API 压测 (需安装 hey) ==="
hey -n 100 -c 10 http://localhost:8080/health
