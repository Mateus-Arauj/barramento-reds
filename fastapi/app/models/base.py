"""
Base para modelos SQLAlchemy
"""
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class TimestampMixin:
    """
    Mixin para adicionar campos de auditoria a modelos
    """
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FHIRResourceMixin:
    """
    Mixin para campos comuns de recursos FHIR
    """
    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)


def generate_uuid():
    """
    Gera um UUID v4 como string
    """
    return str(uuid.uuid4())
