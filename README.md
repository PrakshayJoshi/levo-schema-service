# Levo Schema Service (Fixed)

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
pip install -r requirements.txt
uvicorn app.main:app --reload
```
# levo-schema-service
