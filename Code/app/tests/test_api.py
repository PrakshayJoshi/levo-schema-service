import io, json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

valid_schema = {
    "openapi": "3.0.0",
    "info": {"title": "Test API", "version": "1.0.0"},
    "paths": {}
}

def test_root():
    r = client.get("/")
    assert r.status_code == 200

def test_import_and_get_latest():
    file_content = json.dumps(valid_schema).encode()
    r = client.post("/schemas/import",
                    data={"application": "testapp", "service": "svc"},
                    files={"file": ("openapi.json", file_content, "application/json")})
    assert r.status_code == 200
    latest = client.get("/schemas/testapp/svc/latest")
    assert latest.status_code == 200
    assert latest.json()["openapi"] == "3.0.0"

def test_versions_endpoint():
    r = client.get("/schemas/testapp/svc/versions")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
