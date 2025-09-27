from fastapi import FastAPI
from app.routes import router
from app.database import Base, engine

app = FastAPI(title="Levo Schema Service")

# Create tables
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Levo Schema Service running"}
