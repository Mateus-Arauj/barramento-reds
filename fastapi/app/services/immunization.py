"""
Service para recurso FHIR Immunization
"""
from datetime import datetime
from fastapi import HTTPException
import uuid

from app.repositories.immunization import ImmunizationRepository
from app.repositories.patient import PatientRepository
from app.models.immunization import Immunization
from app.schemas.immunization import ImmunizationResource


class ImmunizationService:
    def __init__(self, repository: ImmunizationRepository, patient_repository: PatientRepository):
        self.repository = repository
        self.patient_repository = patient_repository

    def _extract_id(self, reference: str) -> str:
        if reference and "/" in reference:
            return reference.split("/")[-1]
        return reference

    def create(self, immunization: ImmunizationResource) -> Immunization:
        imm_id = immunization.id or str(uuid.uuid4())

        patient_id = None
        subject_reference = None
        if immunization.patient and immunization.patient.reference:
            subject_reference = immunization.patient.reference
            patient_id = self._extract_id(subject_reference)
            patient = self.patient_repository.get_by_id(patient_id)
            if not patient:
                raise HTTPException(status_code=400, detail=f"Patient/{patient_id} not found")

        encounter_id = None
        if immunization.encounter and immunization.encounter.reference:
            encounter_id = self._extract_id(immunization.encounter.reference)

        imm_data = immunization.model_dump(exclude_none=True, by_alias=True)
        imm_data["id"] = imm_id
        imm_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_imm = Immunization(
            id=imm_id,
            identifier=imm_data.get("identifier"),
            status=immunization.status,
            status_reason=imm_data.get("statusReason"),
            vaccine_code=imm_data.get("vaccineCode"),
            subject_reference=subject_reference,
            patient_id=patient_id,
            encounter_id=encounter_id,
            occurrence_datetime=immunization.occurrenceDateTime,
            occurrence_string=immunization.occurrenceString,
            recorded=immunization.recorded,
            primary_source=str(immunization.primarySource) if immunization.primarySource is not None else None,
            report_origin=imm_data.get("reportOrigin"),
            location=imm_data.get("location"),
            manufacturer=imm_data.get("manufacturer"),
            lot_number=immunization.lotNumber,
            expiration_date=immunization.expirationDate,
            site=imm_data.get("site"),
            route=imm_data.get("route"),
            dose_quantity=imm_data.get("doseQuantity"),
            performer=imm_data.get("performer"),
            note=imm_data.get("note"),
            reason_code=imm_data.get("reasonCode"),
            reason_reference=imm_data.get("reasonReference"),
            is_subpotent=str(immunization.isSubpotent) if immunization.isSubpotent is not None else None,
            subpotent_reason=imm_data.get("subpotentReason"),
            education=imm_data.get("education"),
            program_eligibility=imm_data.get("programEligibility"),
            funding_source=imm_data.get("fundingSource"),
            reaction=imm_data.get("reaction"),
            protocol_applied=imm_data.get("protocolApplied"),
            meta=imm_data.get("meta"),
            resource_json=imm_data
        )
        return self.repository.create(db_imm)

    def get_by_id(self, imm_id: str) -> Immunization:
        return self.repository.get_by_id_or_404(imm_id)

    def update(self, imm_id: str, immunization: ImmunizationResource) -> Immunization:
        db_imm = self.repository.get_by_id_or_404(imm_id)
        imm_data = immunization.model_dump(exclude_none=True, by_alias=True)
        imm_data["id"] = imm_id

        current_version = 1
        if db_imm.meta and "versionId" in db_imm.meta:
            current_version = int(db_imm.meta["versionId"]) + 1
        imm_data["meta"] = {
            "versionId": str(current_version),
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_imm.status = immunization.status
        db_imm.vaccine_code = imm_data.get("vaccineCode")
        db_imm.occurrence_datetime = immunization.occurrenceDateTime
        db_imm.lot_number = immunization.lotNumber
        db_imm.expiration_date = immunization.expirationDate
        db_imm.site = imm_data.get("site")
        db_imm.route = imm_data.get("route")
        db_imm.dose_quantity = imm_data.get("doseQuantity")
        db_imm.performer = imm_data.get("performer")
        db_imm.note = imm_data.get("note")
        db_imm.protocol_applied = imm_data.get("protocolApplied")
        db_imm.meta = imm_data.get("meta")
        db_imm.resource_json = imm_data
        return self.repository.update(db_imm)

    def delete(self, imm_id: str) -> None:
        self.repository.delete_by_id(imm_id, "Immunization")

    def search(self, patient=None, status=None, vaccine_code=None, date=None, limit=50):
        patient_id = self._extract_id(patient) if patient else None
        return self.repository.search(
            patient_id=patient_id, status=status,
            vaccine_code=vaccine_code, date=date, limit=limit
        )
