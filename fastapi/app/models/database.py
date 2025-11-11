"""
Modelos SQLAlchemy para armazenar recursos FHIR (Patient e Observation)
"""
from sqlalchemy import Column, String, Text, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class Patient(Base):
    """
    Modelo para armazenar recursos FHIR Patient
    """
    __tablename__ = "patients"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    resource_type = Column(String(50), nullable=False, default="Patient")
    
    identifier = Column(JSON)
    active = Column(String(10))
    name = Column(JSON)
    telecom = Column(JSON)
    gender = Column(String(20))
    birth_date = Column(String(20))
    address = Column(JSON)
    
    meta = Column(JSON)
    
    resource_json = Column(JSON, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    observations = relationship("Observation", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient(id={self.id}, name={self.name})>"


class Observation(Base):
    """
    Modelo para armazenar recursos FHIR Observation
    """
    __tablename__ = "observations"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    resource_type = Column(String(50), nullable=False, default="Observation")
    
    identifier = Column(JSON)
    status = Column(String(20))
    category = Column(JSON)
    code = Column(JSON)
    
    subject_reference = Column(String(255))
    patient_id = Column(String(64), ForeignKey("patients.id"), nullable=True)
    
    effective_datetime = Column(String(50))
    effective_period = Column(JSON)
    issued = Column(String(50))
    
    value_quantity = Column(JSON)
    value_codeable_concept = Column(JSON)
    value_string = Column(Text)
    value_boolean = Column(String(10))
    value_integer = Column(Integer)
    value_range = Column(JSON)
    value_ratio = Column(JSON)
    value_sampled_data = Column(JSON)
    value_time = Column(String(20))
    value_datetime = Column(String(50))
    value_period = Column(JSON)
    
    interpretation = Column(JSON)
    note = Column(JSON)
    
    meta = Column(JSON)
    
    resource_json = Column(JSON, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="observations")

    def __repr__(self):
        return f"<Observation(id={self.id}, status={self.status})>"
