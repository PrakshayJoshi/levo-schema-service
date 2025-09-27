import os, yaml
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services import parse_and_validate, save_file

router = APIRouter(prefix="/schemas", tags=["schemas"])
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

def get_or_create_app(db: Session, name: str):
    app_obj = db.query(models.Application).filter_by(name=name).first()
    if not app_obj:
        app_obj = models.Application(name=name)
        db.add(app_obj)
        db.commit()
        db.refresh(app_obj)
    return app_obj

def get_or_create_service(db: Session, app_obj, service: str):
    if not service:
        return None
    svc = db.query(models.Service).filter_by(name=service, application_id=app_obj.id).first()
    if not svc:
        svc = models.Service(name=service, application_id=app_obj.id)
        db.add(svc)
        db.commit()
        db.refresh(svc)
    return svc

def get_next_version(db: Session, app_id: int, service_id: int = None):
    q = db.query(models.Schema).filter_by(application_id=app_id)
    if service_id:
        q = q.filter_by(service_id=service_id)
    latest = q.order_by(models.Schema.version.desc()).first()
    return (latest.version + 1) if latest else 1

@router.post("/import")
async def import_schema(application: str = Form(...), service: str = Form(None),
                        replace: bool = Form(False), file: UploadFile = File(...),
                        db: Session = Depends(get_db)):
    app_obj = get_or_create_app(db, application)
    service_obj = get_or_create_service(db, app_obj, service)

    content = await file.read()
    try:
        schema_dict, warning = parse_and_validate(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    version = get_next_version(db, app_obj.id, service_obj.id if service_obj else None)
    if replace and version > 1:
        version -= 1

    ext = file.filename.split(".")[-1]
    save_path = save_file(STORAGE_DIR, application, service, version, ext, content)

    schema_entry = models.Schema(
        version=version, file_path=save_path,
        application_id=app_obj.id, service_id=service_obj.id if service_obj else None
    )
    db.add(schema_entry)
    db.commit()
    db.refresh(schema_entry)

    resp = {"message": "Schema imported", "version": version}
    if warning:
        resp["warning"] = f"Schema validation issue: {warning}"
    return resp

@router.get("/{application}/{service}/versions")
def list_versions(application: str, service: str, db: Session = Depends(get_db)):
    app_obj = db.query(models.Application).filter_by(name=application).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    svc = db.query(models.Service).filter_by(name=service, application_id=app_obj.id).first()
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    schemas = db.query(models.Schema).filter_by(application_id=app_obj.id, service_id=svc.id).all()
    return [{"version": s.version, "file_path": s.file_path} for s in schemas]

@router.get("/{application}/{service}/latest")
def get_latest(application: str, service: str, db: Session = Depends(get_db)):
    app_obj = db.query(models.Application).filter_by(name=application).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    svc = db.query(models.Service).filter_by(name=service, application_id=app_obj.id).first()
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    schema = db.query(models.Schema).filter_by(application_id=app_obj.id, service_id=svc.id)        .order_by(models.Schema.version.desc()).first()
    if not schema:
        raise HTTPException(status_code=404, detail="No schema found")
    with open(schema.file_path, "r") as f:
        return yaml.safe_load(f)

@router.get("/{application}/{service}/{version}")
def get_version(application: str, service: str, version: int, db: Session = Depends(get_db)):
    app_obj = db.query(models.Application).filter_by(name=application).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    svc = db.query(models.Service).filter_by(name=service, application_id=app_obj.id).first()
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    schema = db.query(models.Schema).filter_by(application_id=app_obj.id, service_id=svc.id, version=version).first()
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    with open(schema.file_path, "r") as f:
        return yaml.safe_load(f)
