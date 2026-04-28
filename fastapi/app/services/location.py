"""
Service para recurso FHIR Location
"""
from datetime import datetime
import uuid

from app.repositories.location import LocationRepository
from app.models.location import Location
from app.schemas.location import LocationResource


class LocationService:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    def create(self, location: LocationResource) -> Location:
        loc_id = location.id or str(uuid.uuid4())
        loc_data = location.model_dump(exclude_none=True, by_alias=True)
        loc_data["id"] = loc_id
        loc_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        managing_org_id = None
        if location.managingOrganization and location.managingOrganization.reference:
            ref = location.managingOrganization.reference
            if "/" in ref:
                managing_org_id = ref.split("/")[-1]

        db_loc = Location(
            id=loc_id,
            identifier=loc_data.get("identifier"),
            status=location.status,
            operational_status=loc_data.get("operationalStatus"),
            name=location.name,
            alias=loc_data.get("alias"),
            description=location.description,
            mode=location.mode,
            type=loc_data.get("type"),
            telecom=loc_data.get("telecom"),
            address=loc_data.get("address"),
            physical_type=loc_data.get("physicalType"),
            position=loc_data.get("position"),
            managing_organization_id=managing_org_id,
            managing_organization=loc_data.get("managingOrganization"),
            part_of=loc_data.get("partOf"),
            hours_of_operation=loc_data.get("hoursOfOperation"),
            availability_exceptions=location.availabilityExceptions,
            endpoint=loc_data.get("endpoint"),
            meta=loc_data.get("meta"),
            resource_json=loc_data
        )
        return self.repository.create(db_loc)

    def get_by_id(self, loc_id: str) -> Location:
        return self.repository.get_by_id_or_404(loc_id)

    def update(self, loc_id: str, location: LocationResource) -> Location:
        db_loc = self.repository.get_by_id_or_404(loc_id)
        loc_data = location.model_dump(exclude_none=True, by_alias=True)
        loc_data["id"] = loc_id

        current_version = 1
        if db_loc.meta and "versionId" in db_loc.meta:
            current_version = int(db_loc.meta["versionId"]) + 1
        loc_data["meta"] = {
            "versionId": str(current_version),
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_loc.identifier = loc_data.get("identifier")
        db_loc.status = location.status
        db_loc.operational_status = loc_data.get("operationalStatus")
        db_loc.name = location.name
        db_loc.alias = loc_data.get("alias")
        db_loc.description = location.description
        db_loc.mode = location.mode
        db_loc.type = loc_data.get("type")
        db_loc.telecom = loc_data.get("telecom")
        db_loc.address = loc_data.get("address")
        db_loc.physical_type = loc_data.get("physicalType")
        db_loc.position = loc_data.get("position")
        db_loc.managing_organization = loc_data.get("managingOrganization")
        db_loc.part_of = loc_data.get("partOf")
        db_loc.hours_of_operation = loc_data.get("hoursOfOperation")
        db_loc.availability_exceptions = location.availabilityExceptions
        db_loc.endpoint = loc_data.get("endpoint")
        db_loc.meta = loc_data.get("meta")
        db_loc.resource_json = loc_data
        return self.repository.update(db_loc)

    def delete(self, loc_id: str) -> None:
        self.repository.delete_by_id(loc_id, "Location")

    def search(self, name=None, status=None, organization=None, type_code=None, limit=50):
        return self.repository.search(
            name=name, status=status, organization=organization,
            type_code=type_code, limit=limit
        )
