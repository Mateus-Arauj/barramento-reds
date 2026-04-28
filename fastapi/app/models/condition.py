"""
Modelo SQLAlchemy para recurso FHIR Condition (Diagnóstico - CID-10/CIAP-2)
"""
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class Condition(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR Condition
    Representa diagnósticos e problemas de saúde (CID-10, CIAP-2)
    """
    __tablename__ = "conditions"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="Condition")

    identifier = Column(JSON)
    clinical_status = Column(JSON)  # active | recurrence | relapse | inactive | remission | resolved
    verification_status = Column(JSON)  # unconfirmed | provisional | differential | confirmed | refuted | entered-in-error
    category = Column(JSON)  # problem-list-item | encounter-diagnosis
    severity = Column(JSON)
    code = Column(JSON)  # CID-10, CIAP-2

    subject_reference = Column(String(255))
    patient_id = Column(String(64), ForeignKey("patients.id"), nullable=True)
    encounter_id = Column(String(64), ForeignKey("encounters.id"), nullable=True)

    onset_datetime = Column(String(50))
    onset_age = Column(JSON)
    onset_period = Column(JSON)
    onset_range = Column(JSON)
    onset_string = Column(String(255))

    abatement_datetime = Column(String(50))
    abatement_age = Column(JSON)
    abatement_period = Column(JSON)
    abatement_range = Column(JSON)
    abatement_string = Column(String(255))

    recorded_date = Column(String(50))
    recorder = Column(JSON)
    asserter = Column(JSON)
    stage = Column(JSON)
    evidence = Column(JSON)
    note = Column(JSON)
    body_site = Column(JSON)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    patient = relationship("Patient", foreign_keys=[patient_id])

    def __repr__(self):
        return f"<Condition(id={self.id}, code={self.code})>"
