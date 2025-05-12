#!/usr/bin/env bash
# Test /api/search_data/ endpoint with 1, 2, and 5 files

BASE_URL="http://localhost:8000/api/search_data/"

echo "== Single file upload =="
curl -s -X POST "$BASE_URL" \
     -F "file=@/mnt/data/example.txt" \
     -F "query=Retrieval-Augmented Generation" \
     -H "Content-Type: multipart/form-data" | jq

echo "\n== Two files upload =="
curl -s -X POST "$BASE_URL" \
     -F "file=@/mnt/data/example.txt" \
     -F "file=@/mnt/data/example.html" \
     -F "query=vector search" \
     -H "Content-Type: multipart/form-data" | jq

echo "\n== Five files upload =="
curl -s -X POST "$BASE_URL" \
     -F "file=@/mnt/data/example.txt" \
     -F "file=@/mnt/data/example.html" \
     -F "file=@/mnt/data/example.csv" \
     -F "file=@/mnt/data/example.xlsx" \
     -F "file=@/mnt/data/example.pdf" \
     -F "query=hybrid search" \
     -H "Content-Type: multipart/form-data" | jq
