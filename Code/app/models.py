from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    services = relationship("Service", back_populates="application")
    schemas = relationship("Schema", back_populates="application")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    application = relationship("Application", back_populates="services")
    schemas = relationship("Schema", back_populates="service")

class Schema(Base):
    __tablename__ = "schemas"
    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer)
    file_path = Column(String)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    application_id = Column(Integer, ForeignKey("applications.id"))
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    application = relationship("Application", back_populates="schemas")
    service = relationship("Service", back_populates="schemas")
