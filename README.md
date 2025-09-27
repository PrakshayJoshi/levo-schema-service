# Levo Schema Service

Implements upload/versioning API for OpenAPI schemas.

## Features
- Upload OpenAPI schemas (JSON/YAML)
- Validate schemas (non-compliant allowed with warnings)
- Version or replace schemas
- Store schemas in filesystem + SQLite
- Retrieve latest or specific version
- List versions
- Unit tests

## CLI mapping
- `levo import --spec openapi.yaml --application app --service svc`
  → POST /schemas/import
- `levo test --application app --service svc`
  → GET /schemas/app/svc/latest

## Run
```bash
cd Code
python3 -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## This project includes unit tests (pytest) for all requirements

# Linux / macOS
PYTHONPATH=. pytest -v
## Windows (PowerShell)
$env:PYTHONPATH="."; pytest -v

## Run Demo Script
chmod +x test_api_flow.sh
./test_api_flow.sh


# levo-schema-service
