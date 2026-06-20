"""
Modelo SQLAlchemy para recurso FHIR Organization (BR Core: Estabelecimento de Saúde)
"""
from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin, generate_uuid


class Organization(Base, TimestampMixin):
    """
    Modelo para armazenar recursos FHIR Organization
    Representa estabelecimentos de saúde (hospitais, UBS, clínicas, etc.)
    """
    __tablename__ = "organizations"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    resource_type = Column(String(50), nullable=False, default="Organization")

    identifier = Column(JSON)  # CNES, CNPJ
    active = Column(String(10))
    type = Column(JSON)  # Tipo de estabelecimento
    name = Column(String(255))
    alias = Column(JSON)  # Nomes alternativos
    telecom = Column(JSON)
    address = Column(JSON)
    part_of = Column(JSON)  # Organização pai (referência)
    contact = Column(JSON)
    endpoint = Column(JSON)

    meta = Column(JSON)
    resource_json = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<Organization(id={self.id}, name={self.name})>"
