#!/usr/bin/env bash
# Test /api/chat_llm/ endpoint with single file and prompt

BASE_URL="http://localhost:8000/api/chat_llm/"

echo "== Chat LLM single file =="
curl -s -X POST "$BASE_URL" \
     -F "file=@/mnt/data/example.txt" \
     -F "query=Explain RAG" \
     -F "prompt=Answer as a machine learning expert." \
     -H "Content-Type: multipart/form-data" | jq
