"""
Service para recurso FHIR Practitioner
"""
from datetime import datetime
import uuid

from app.repositories.practitioner import PractitionerRepository
from app.models.practitioner import Practitioner
from app.schemas.practitioner import PractitionerResource


class PractitionerService:
    """
    Serviço com lógica de negócio para recursos Practitioner
    """

    def __init__(self, repository: PractitionerRepository):
        """
        Inicializa o service com repository injetado
        """
        self.repository = repository

    def create(self, practitioner: PractitionerResource) -> Practitioner:
        """
        Cria um novo recurso Practitioner
        """
        practitioner_id = practitioner.id or str(uuid.uuid4())

        practitioner_data = practitioner.model_dump(exclude_none=True, by_alias=True)
        practitioner_data["id"] = practitioner_id
        practitioner_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_practitioner = Practitioner(
            id=practitioner_id,
            identifier=practitioner_data.get("identifier"),
            active=str(practitioner.active) if practitioner.active is not None else None,
            name=practitioner_data.get("name"),
            telecom=practitioner_data.get("telecom"),
            address=practitioner_data.get("address"),
            gender=practitioner.gender,
            birth_date=practitioner.birthDate,
            photo=practitioner_data.get("photo"),
            qualification=practitioner_data.get("qualification"),
            communication=practitioner_data.get("communication"),
            meta=practitioner_data.get("meta"),
            resource_json=practitioner_data
        )

        return self.repository.create(db_practitioner)

    def get_by_id(self, practitioner_id: str) -> Practitioner:
        """
        Recupera um Practitioner por ID
        """
        return self.repository.get_by_id_or_404(practitioner_id)

    def update(self, practitioner_id: str, practitioner: PractitionerResource) -> Practitioner:
        """
        Atualiza um Practitioner existente
        """
        db_practitioner = self.repository.get_by_id_or_404(practitioner_id)

        practitioner_data = practitioner.model_dump(exclude_none=True, by_alias=True)
        practitioner_data["id"] = practitioner_id

        current_version = 1
        if db_practitioner.meta and "versionId" in db_practitioner.meta:
            current_version = int(db_practitioner.meta["versionId"]) + 1

        practitioner_data["meta"] = {
            "versionId": str(current_version),
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_practitioner.identifier = practitioner_data.get("identifier")
        db_practitioner.active = str(practitioner.active) if practitioner.active is not None else None
        db_practitioner.name = practitioner_data.get("name")
        db_practitioner.telecom = practitioner_data.get("telecom")
        db_practitioner.address = practitioner_data.get("address")
        db_practitioner.gender = practitioner.gender
        db_practitioner.birth_date = practitioner.birthDate
        db_practitioner.photo = practitioner_data.get("photo")
        db_practitioner.qualification = practitioner_data.get("qualification")
        db_practitioner.communication = practitioner_data.get("communication")
        db_practitioner.meta = practitioner_data.get("meta")
        db_practitioner.resource_json = practitioner_data

        return self.repository.update(db_practitioner)

    def delete(self, practitioner_id: str) -> None:
        """
        Remove um Practitioner
        """
        self.repository.delete_by_id(practitioner_id, "Practitioner")

    def search(
        self,
        name: str = None,
        identifier: str = None,
        active: bool = None,
        limit: int = 50
    ) -> list:
        """
        Busca Practitioners com filtros
        """
        return self.repository.search(
            name=name,
            identifier=identifier,
            active=active,
            limit=limit
        )
