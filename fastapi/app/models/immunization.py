"""
Modelo SQLAlchemy para recurso FHIR Immunization (Imunização - PNI)
"""
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class Immunization(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR Immunization
    Representa imunobiológicos administrados (PNI - Programa Nacional de Imunizações)
    """
    __tablename__ = "immunizations"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="Immunization")

    identifier = Column(JSON)
    status = Column(String(20))  # completed | entered-in-error | not-done
    status_reason = Column(JSON)
    vaccine_code = Column(JSON)  # Código do imunobiológico (PNI)

    subject_reference = Column(String(255))
    patient_id = Column(String(64), ForeignKey("patients.id"), nullable=True)
    encounter_id = Column(String(64), ForeignKey("encounters.id"), nullable=True)

    occurrence_datetime = Column(String(50))
    occurrence_string = Column(String(255))
    recorded = Column(String(50))
    primary_source = Column(String(10))
    report_origin = Column(JSON)
    location = Column(JSON)
    manufacturer = Column(JSON)
    lot_number = Column(String(100))
    expiration_date = Column(String(20))
    site = Column(JSON)  # Local de aplicação
    route = Column(JSON)  # Via de administração
    dose_quantity = Column(JSON)
    performer = Column(JSON)
    note = Column(JSON)
    reason_code = Column(JSON)
    reason_reference = Column(JSON)
    is_subpotent = Column(String(10))
    subpotent_reason = Column(JSON)
    education = Column(JSON)
    program_eligibility = Column(JSON)
    funding_source = Column(JSON)
    reaction = Column(JSON)
    protocol_applied = Column(JSON)  # Dose na série (1ª dose, 2ª dose, reforço)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    patient = relationship("Patient", foreign_keys=[patient_id])

    def __repr__(self):
        return f"<Immunization(id={self.id}, status={self.status})>"
