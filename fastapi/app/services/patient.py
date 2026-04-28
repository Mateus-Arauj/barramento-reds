"""
Service para recurso FHIR Patient
"""
from datetime import datetime
import uuid

from app.repositories.patient import PatientRepository
from app.models.patient import Patient
from app.schemas.patient import PatientResource


class PatientService:
    """
    Serviço com lógica de negócio para recursos Patient
    """

    def __init__(self, repository: PatientRepository):
        """
        Inicializa o service com repository injetado
        """
        self.repository = repository

    def create(self, patient: PatientResource) -> Patient:
        """
        Cria um novo recurso Patient
        """
        patient_id = patient.id or str(uuid.uuid4())

        patient_data = patient.model_dump(exclude_none=True, by_alias=True)
        patient_data["id"] = patient_id
        patient_data["meta"] = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_patient = Patient(
            id=patient_id,
            identifier=patient_data.get("identifier"),
            active=str(patient.active) if patient.active is not None else None,
            name=patient_data.get("name"),
            telecom=patient_data.get("telecom"),
            gender=patient.gender,
            birth_date=patient.birthDate,
            address=patient_data.get("address"),
            marital_status=patient_data.get("maritalStatus"),
            deceased_boolean=str(patient.deceasedBoolean) if patient.deceasedBoolean is not None else None,
            deceased_datetime=patient.deceasedDateTime,
            multiple_birth_boolean=str(patient.multipleBirthBoolean) if patient.multipleBirthBoolean is not None else None,
            multiple_birth_integer=str(patient.multipleBirthInteger) if patient.multipleBirthInteger is not None else None,
            contact=patient_data.get("contact"),
            communication=patient_data.get("communication"),
            general_practitioner=patient_data.get("generalPractitioner"),
            managing_organization=patient_data.get("managingOrganization"),
            mother_name=patient.motherName,
            father_name=patient.fatherName,
            nationality=patient_data.get("nationality"),
            race=patient_data.get("race"),
            ethnicity=patient_data.get("ethnicity"),
            birth_city=patient_data.get("birthCity"),
            meta=patient_data.get("meta"),
            resource_json=patient_data
        )

        return self.repository.create(db_patient)

    def get_by_id(self, patient_id: str) -> Patient:
        """
        Recupera um Patient por ID
        """
        return self.repository.get_by_id_or_404(patient_id)

    def update(self, patient_id: str, patient: PatientResource) -> Patient:
        """
        Atualiza um Patient existente
        """
        db_patient = self.repository.get_by_id_or_404(patient_id)

        patient_data = patient.model_dump(exclude_none=True, by_alias=True)
        patient_data["id"] = patient_id

        current_version = 1
        if db_patient.meta and "versionId" in db_patient.meta:
            current_version = int(db_patient.meta["versionId"]) + 1

        patient_data["meta"] = {
            "versionId": str(current_version),
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }

        db_patient.identifier = patient_data.get("identifier")
        db_patient.active = str(patient.active) if patient.active is not None else None
        db_patient.name = patient_data.get("name")
        db_patient.telecom = patient_data.get("telecom")
        db_patient.gender = patient.gender
        db_patient.birth_date = patient.birthDate
        db_patient.address = patient_data.get("address")
        db_patient.marital_status = patient_data.get("maritalStatus")
        db_patient.deceased_boolean = str(patient.deceasedBoolean) if patient.deceasedBoolean is not None else None
        db_patient.deceased_datetime = patient.deceasedDateTime
        db_patient.multiple_birth_boolean = str(patient.multipleBirthBoolean) if patient.multipleBirthBoolean is not None else None
        db_patient.multiple_birth_integer = str(patient.multipleBirthInteger) if patient.multipleBirthInteger is not None else None
        db_patient.contact = patient_data.get("contact")
        db_patient.communication = patient_data.get("communication")
        db_patient.general_practitioner = patient_data.get("generalPractitioner")
        db_patient.managing_organization = patient_data.get("managingOrganization")
        db_patient.mother_name = patient.motherName
        db_patient.father_name = patient.fatherName
        db_patient.nationality = patient_data.get("nationality")
        db_patient.race = patient_data.get("race")
        db_patient.ethnicity = patient_data.get("ethnicity")
        db_patient.birth_city = patient_data.get("birthCity")
        db_patient.meta = patient_data.get("meta")
        db_patient.resource_json = patient_data

        return self.repository.update(db_patient)

    def delete(self, patient_id: str) -> None:
        """
        Remove um Patient
        """
        self.repository.delete_by_id(patient_id, "Patient")

    def search(
        self,
        name: str = None,
        gender: str = None,
        birthdate: str = None,
        limit: int = 50
    ) -> list:
        """
        Busca Patients com filtros
        """
        return self.repository.search(
            name=name,
            gender=gender,
            birthdate=birthdate,
            limit=limit
        )
