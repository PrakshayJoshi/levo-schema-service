import os, json, yaml
from openapi_spec_validator.shortcuts import validate

def parse_and_validate(file_bytes: bytes, filename: str):
    try:
        if filename.endswith((".yaml", ".yml")):
            schema_dict = yaml.safe_load(file_bytes)
        else:
            schema_dict = json.loads(file_bytes)
    except Exception:
        raise ValueError("Invalid JSON/YAML schema")

    warning = None
    try:
        validate_spec(schema_dict)
    except Exception as e:
        # Keep warning but don't block upload
        warning = str(e)

    return schema_dict, warning

def save_file(base_dir: str, application: str, service: str, version: int, ext: str, content: bytes):
    save_dir = os.path.join(base_dir, application, service or "root")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"v{version}.{ext}")
    with open(save_path, "wb") as f:
        f.write(content)
    return save_path
