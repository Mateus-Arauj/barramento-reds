"""
Service para recurso FHIR Organization
"""
from datetime import datetime
import uuid

from app.repositories.organization import OrganizationRepository
from app.models.organization import Organization
from app.schemas.organization import OrganizationResource


class OrganizationService:
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository

    def create(self, organization: OrganizationResource) -> Organization:
        org_id = organization.id or str(uuid.uuid4())
        org_data = organization.model_dump(exclude_none=True, by_alias=True)
        org_data["id"] = org_id
        org_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_org = Organization(
            id=org_id,
            identifier=org_data.get("identifier"),
            active=str(organization.active) if organization.active is not None else None,
            type=org_data.get("type"),
            name=organization.name,
            alias=org_data.get("alias"),
            telecom=org_data.get("telecom"),
            address=org_data.get("address"),
            part_of=org_data.get("partOf"),
            contact=org_data.get("contact"),
            endpoint=org_data.get("endpoint"),
            meta=org_data.get("meta"),
            resource_json=org_data
        )
        return self.repository.create(db_org)

    def get_by_id(self, org_id: str) -> Organization:
        return self.repository.get_by_id_or_404(org_id)

    def update(self, org_id: str, organization: OrganizationResource) -> Organization:
        db_org = self.repository.get_by_id_or_404(org_id)
        org_data = organization.model_dump(exclude_none=True, by_alias=True)
        org_data["id"] = org_id

        current_version = 1
        if db_org.meta and "versionId" in db_org.meta:
            current_version = int(db_org.meta["versionId"]) + 1
        org_data["meta"] = {
            "versionId": str(current_version),
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_org.identifier = org_data.get("identifier")
        db_org.active = str(organization.active) if organization.active is not None else None
        db_org.type = org_data.get("type")
        db_org.name = organization.name
        db_org.alias = org_data.get("alias")
        db_org.telecom = org_data.get("telecom")
        db_org.address = org_data.get("address")
        db_org.part_of = org_data.get("partOf")
        db_org.contact = org_data.get("contact")
        db_org.endpoint = org_data.get("endpoint")
        db_org.meta = org_data.get("meta")
        db_org.resource_json = org_data
        return self.repository.update(db_org)

    def delete(self, org_id: str) -> None:
        self.repository.delete_by_id(org_id, "Organization")

    def search(self, name=None, identifier=None, active=None, type_code=None, limit=50):
        return self.repository.search(
            name=name, identifier=identifier, active=active,
            type_code=type_code, limit=limit
        )
