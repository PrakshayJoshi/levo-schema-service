#!/bin/bash
# test_api_flow.sh
# Demo script for Levo Schema Service API

BASE_URL="http://127.0.0.1:8000"

echo "==== Health Check ===="
curl -s $BASE_URL/ | jq

echo -e "\n==== Upload Schema (JSON) ===="
curl -s -X POST "$BASE_URL/schemas/import" \
  -F "application=crAPI" \
  -F "service=auth" \
  -F "file=@openapi.json" | jq

echo -e "\n==== Upload Schema (YAML) ===="
curl -s -X POST "$BASE_URL/schemas/import" \
  -F "application=crAPI" \
  -F "service=auth" \
  -F "file=@openapi.yaml" | jq

echo -e "\n==== Replace Schema (JSON) ===="
curl -s -X POST "$BASE_URL/schemas/import" \
  -F "application=crAPI" \
  -F "service=auth" \
  -F "replace=true" \
  -F "file=@openapi.json" | jq

echo -e "\n==== Get Latest Schema ===="
curl -s $BASE_URL/schemas/crAPI/auth/latest | jq

echo -e "\n==== Get Specific Version (1) ===="
curl -s $BASE_URL/schemas/crAPI/auth/1 | jq

echo -e "\n==== List All Versions ===="
curl -s $BASE_URL/schemas/crAPI/auth/versions | jq

echo -e "\n==== Invalid Schema Upload (warning expected) ===="
echo '{"invalid":"schema"}' > invalid.json
curl -s -X POST "$BASE_URL/schemas/import" \
  -F "application=testapp" \
  -F "service=svc" \
  -F "file=@invalid.json" | jq

echo -e "\n==== Fetch Non-Existent App ===="
curl -s $BASE_URL/schemas/doesnotexist/svc/latest | jq
