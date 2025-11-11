"""
Serviço para manipulação de recursos FHIR Patient
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import Optional
import uuid
from datetime import datetime

from app.models.database import Patient
from app.schemas.patient import PatientResource


class PatientService:
    """
    Serviço para operações com Patient
    """
    
    @staticmethod
    def create_patient(db: Session, patient_data: PatientResource) -> Patient:
        """
        Cria um novo recurso Patient no banco de dados
        """
        if not patient_data.id:
            patient_data.id = str(uuid.uuid4())
        
        if not patient_data.meta:
            patient_data.meta = {}
        
        patient_dict = patient_data.model_dump(exclude_none=True)
        patient_dict['meta'] = patient_dict.get('meta', {})
        patient_dict['meta']['versionId'] = '1'
        patient_dict['meta']['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'
        
        db_patient = Patient(
            id=patient_data.id,
            identifier=patient_dict.get('identifier'),
            active=str(patient_dict.get('active', '')).lower() if patient_dict.get('active') is not None else None,
            name=patient_dict.get('name'),
            telecom=patient_dict.get('telecom'),
            gender=patient_dict.get('gender'),
            birth_date=patient_dict.get('birthDate'),
            address=patient_dict.get('address'),
            meta=patient_dict['meta'],
            resource_json=patient_dict
        )
        
        try:
            db.add(db_patient)
            db.commit()
            db.refresh(db_patient)
            return db_patient
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=409, detail=f"Patient with id {patient_data.id} already exists")
    
    @staticmethod
    def get_patient(db: Session, patient_id: str) -> Optional[Patient]:
        """
        Busca um Patient por ID
        """
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail=f"Patient/{patient_id} not found")
        return patient
    
    @staticmethod
    def update_patient(db: Session, patient_id: str, patient_data: PatientResource) -> Patient:
        """
        Atualiza um Patient existente
        """
        db_patient = PatientService.get_patient(db, patient_id)
        
        patient_dict = patient_data.model_dump(exclude_none=True)
        patient_dict['id'] = patient_id
        
        current_version = int(db_patient.meta.get('versionId', 1))
        patient_dict['meta'] = patient_dict.get('meta', {})
        patient_dict['meta']['versionId'] = str(current_version + 1)
        patient_dict['meta']['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'
        
        db_patient.identifier = patient_dict.get('identifier')
        db_patient.active = str(patient_dict.get('active', '')).lower() if patient_dict.get('active') is not None else None
        db_patient.name = patient_dict.get('name')
        db_patient.telecom = patient_dict.get('telecom')
        db_patient.gender = patient_dict.get('gender')
        db_patient.birth_date = patient_dict.get('birthDate')
        db_patient.address = patient_dict.get('address')
        db_patient.meta = patient_dict['meta']
        db_patient.resource_json = patient_dict
        
        db.commit()
        db.refresh(db_patient)
        return db_patient
    
    @staticmethod
    def delete_patient(db: Session, patient_id: str) -> None:
        """
        Deleta um Patient
        """
        db_patient = PatientService.get_patient(db, patient_id)
        db.delete(db_patient)
        db.commit()
    
    @staticmethod
    def search_patients(
        db: Session,
        name: Optional[str] = None,
        gender: Optional[str] = None,
        birthdate: Optional[str] = None,
        limit: int = 50
    ) -> list[Patient]:
        """
        Busca Patients com filtros
        """
        query = db.query(Patient)
        
        if name:
            query = query.filter(Patient.name.op('@>')(f'[{{"family": "{name}"}}]'))
        
        if gender:
            query = query.filter(Patient.gender == gender)
        
        if birthdate:
            query = query.filter(Patient.birth_date == birthdate)
        
        return query.limit(limit).all()
