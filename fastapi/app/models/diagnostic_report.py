"""
Modelo SQLAlchemy para recurso FHIR DiagnosticReport (Laudo Diagnóstico)
"""
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class DiagnosticReport(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR DiagnosticReport
    Representa laudos de exames laboratoriais e de imagem
    """
    __tablename__ = "diagnostic_reports"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="DiagnosticReport")

    identifier = Column(JSON)
    based_on = Column(JSON)
    status = Column(String(30))  # registered | partial | preliminary | final | amended | corrected | appended | cancelled | entered-in-error | unknown
    category = Column(JSON)
    code = Column(JSON)  # Tipo de laudo

    subject_reference = Column(String(255))
    patient_id = Column(String(64), ForeignKey("patients.id"), nullable=True)
    encounter_id = Column(String(64), ForeignKey("encounters.id"), nullable=True)

    effective_datetime = Column(String(50))
    effective_period = Column(JSON)
    issued = Column(String(50))
    performer = Column(JSON)
    results_interpreter = Column(JSON)
    specimen = Column(JSON)
    result = Column(JSON)  # Referências a Observations
    imaging_study = Column(JSON)
    media = Column(JSON)
    conclusion = Column(String(2000))
    conclusion_code = Column(JSON)
    presented_form = Column(JSON)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    patient = relationship("Patient", foreign_keys=[patient_id])

    def __repr__(self):
        return f"<DiagnosticReport(id={self.id}, status={self.status})>"
