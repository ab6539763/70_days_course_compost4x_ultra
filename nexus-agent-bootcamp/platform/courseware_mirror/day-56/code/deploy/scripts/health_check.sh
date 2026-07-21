#!/bin/bash
curl -sf http://localhost/health && echo "✅ API" || echo "❌ API"
