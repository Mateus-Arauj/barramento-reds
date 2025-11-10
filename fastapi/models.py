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
    
    # Campos principais do recurso Patient
    identifier = Column(JSON)  # Array de identificadores
    active = Column(String(10))  # "true" ou "false"
    name = Column(JSON)  # Array de nomes (HumanName)
    telecom = Column(JSON)  # Array de contatos
    gender = Column(String(20))
    birth_date = Column(String(20))  # Formato: YYYY-MM-DD
    address = Column(JSON)  # Array de endereços
    
    # Metadados
    meta = Column(JSON)  # versionId, lastUpdated, etc.
    
    # Recurso completo em JSON (para facilitar retorno)
    resource_json = Column(JSON, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com Observations
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
    
    # Campos principais do recurso Observation
    identifier = Column(JSON)  # Array de identificadores
    status = Column(String(20))  # registered | preliminary | final | amended
    category = Column(JSON)  # Array de categorias
    code = Column(JSON)  # CodeableConcept - tipo de observação
    
    # Referência ao paciente
    subject_reference = Column(String(255))  # Ex: "Patient/123"
    patient_id = Column(String(64), ForeignKey("patients.id"), nullable=True)
    
    # Contexto temporal
    effective_datetime = Column(String(50))  # ISO 8601
    effective_period = Column(JSON)
    issued = Column(String(50))
    
    # Valor da observação
    value_quantity = Column(JSON)  # Valor numérico com unidade
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
    
    # Interpretação e notas
    interpretation = Column(JSON)
    note = Column(JSON)
    
    # Metadados
    meta = Column(JSON)
    
    # Recurso completo em JSON
    resource_json = Column(JSON, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com Patient
    patient = relationship("Patient", back_populates="observations")

    def __repr__(self):
        return f"<Observation(id={self.id}, status={self.status}, subject={self.subject_reference})>"
