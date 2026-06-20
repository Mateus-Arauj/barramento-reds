"""
Service para recurso FHIR Procedure
"""
from datetime import datetime
from fastapi import HTTPException
import uuid

from app.repositories.procedure import ProcedureRepository
from app.repositories.patient import PatientRepository
from app.models.procedure import Procedure
from app.schemas.procedure import ProcedureResource


class ProcedureService:
    def __init__(self, repository: ProcedureRepository, patient_repository: PatientRepository):
        self.repository = repository
        self.patient_repository = patient_repository

    def _extract_id(self, reference: str) -> str:
        if reference and "/" in reference:
            return reference.split("/")[-1]
        return reference

    def create(self, procedure: ProcedureResource) -> Procedure:
        proc_id = procedure.id or str(uuid.uuid4())

        patient_id = None
        subject_reference = None
        if procedure.subject and procedure.subject.reference:
            subject_reference = procedure.subject.reference
            patient_id = self._extract_id(subject_reference)
            patient = self.patient_repository.get_by_id(patient_id)
            if not patient:
                raise HTTPException(status_code=400, detail=f"Patient/{patient_id} not found")

        encounter_id = None
        if procedure.encounter and procedure.encounter.reference:
            encounter_id = self._extract_id(procedure.encounter.reference)

        proc_data = procedure.model_dump(exclude_none=True, by_alias=True)
        proc_data["id"] = proc_id
        proc_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_proc = Procedure(
            id=proc_id,
            identifier=proc_data.get("identifier"),
            instantiates_canonical=proc_data.get("instantiatesCanonical"),
            instantiates_uri=proc_data.get("instantiatesUri"),
            based_on=proc_data.get("basedOn"),
            part_of=proc_data.get("partOf"),
            status=procedure.status,
            status_reason=proc_data.get("statusReason"),
            category=proc_data.get("category"),
            code=proc_data.get("code"),
            subject_reference=subject_reference,
            patient_id=patient_id,
            encounter_id=encounter_id,
            performed_datetime=procedure.performedDateTime,
            performed_period=proc_data.get("performedPeriod"),
            performed_string=procedure.performedString,
            performed_age=proc_data.get("performedAge"),
            performed_range=proc_data.get("performedRange"),
            recorder=proc_data.get("recorder"),
            asserter=proc_data.get("asserter"),
            performer=proc_data.get("performer"),
            location=proc_data.get("location"),
            reason_code=proc_data.get("reasonCode"),
            reason_reference=proc_data.get("reasonReference"),
            body_site=proc_data.get("bodySite"),
            outcome=proc_data.get("outcome"),
            report=proc_data.get("report"),
            complication=proc_data.get("complication"),
            complication_detail=proc_data.get("complicationDetail"),
            follow_up=proc_data.get("followUp"),
            note=proc_data.get("note"),
            focal_device=proc_data.get("focalDevice"),
            used_reference=proc_data.get("usedReference"),
            used_code=proc_data.get("usedCode"),
            meta=proc_data.get("meta"),
            resource_json=proc_data
        )
        return self.repository.create(db_proc)

    def get_by_id(self, proc_id: str) -> Procedure:
        return self.repository.get_by_id_or_404(proc_id)

    def update(self, proc_id: str, procedure: ProcedureResource) -> Procedure:
        db_proc = self.repository.get_by_id_or_404(proc_id)
        proc_data = procedure.model_dump(exclude_none=True, by_alias=True)
        proc_data["id"] = proc_id

        current_version = 1
        if db_proc.meta and "versionId" in db_proc.meta:
            current_version = int(db_proc.meta["versionId"]) + 1
        proc_data["meta"] = {
            "versionId": str(current_version),
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        patient_id = None
        subject_reference = None
        if procedure.subject and procedure.subject.reference:
            subject_reference = procedure.subject.reference
            patient_id = self._extract_id(subject_reference)

        db_proc.status = procedure.status
        db_proc.code = proc_data.get("code")
        db_proc.subject_reference = subject_reference
        db_proc.patient_id = patient_id
        db_proc.performed_datetime = procedure.performedDateTime
        db_proc.performer = proc_data.get("performer")
        db_proc.reason_code = proc_data.get("reasonCode")
        db_proc.note = proc_data.get("note")
        db_proc.meta = proc_data.get("meta")
        db_proc.resource_json = proc_data
        return self.repository.update(db_proc)

    def delete(self, proc_id: str) -> None:
        self.repository.delete_by_id(proc_id, "Procedure")

    def search(self, patient=None, status=None, code=None, date=None, limit=50):
        patient_id = self._extract_id(patient) if patient else None
        return self.repository.search(
            patient_id=patient_id, status=status,
            code=code, date=date, limit=limit
        )
