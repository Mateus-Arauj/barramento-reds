"""
Serviços para manipulação de recursos FHIR
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import Optional, Dict, Any
import uuid
from datetime import datetime

from models import Patient, Observation
from validators import PatientResource, ObservationResource


class PatientService:
    """Serviço para operações com Patient"""
    
    @staticmethod
    def create_patient(db: Session, patient_data: PatientResource) -> Patient:
        """
        Cria um novo recurso Patient no banco de dados
        """
        # Gera ID se não fornecido
        if not patient_data.id:
            patient_data.id = str(uuid.uuid4())
        
        # Adiciona metadados
        if not patient_data.meta:
            patient_data.meta = {}
        
        patient_dict = patient_data.model_dump(exclude_none=True)
        patient_dict['meta'] = patient_dict.get('meta', {})
        patient_dict['meta']['versionId'] = '1'
        patient_dict['meta']['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Extrai campos para colunas indexadas
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
        
        # Atualiza metadados
        patient_dict = patient_data.model_dump(exclude_none=True)
        patient_dict['id'] = patient_id
        
        current_version = int(db_patient.meta.get('versionId', 1))
        patient_dict['meta'] = patient_dict.get('meta', {})
        patient_dict['meta']['versionId'] = str(current_version + 1)
        patient_dict['meta']['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Atualiza campos
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
    def search_patients(db: Session, name: Optional[str] = None, 
                       gender: Optional[str] = None, 
                       birthdate: Optional[str] = None,
                       limit: int = 50) -> list[Patient]:
        """
        Busca Patients com filtros
        """
        query = db.query(Patient)
        
        if name:
            # Busca em JSON usando operadores PostgreSQL
            query = query.filter(Patient.name.op('@>')(f'[{{"family": "{name}"}}]'))
        
        if gender:
            query = query.filter(Patient.gender == gender)
        
        if birthdate:
            query = query.filter(Patient.birth_date == birthdate)
        
        return query.limit(limit).all()


class ObservationService:
    """Serviço para operações com Observation"""
    
    @staticmethod
    def create_observation(db: Session, observation_data: ObservationResource) -> Observation:
        """
        Cria um novo recurso Observation no banco de dados
        """
        # Gera ID se não fornecido
        if not observation_data.id:
            observation_data.id = str(uuid.uuid4())
        
        # Adiciona metadados
        if not observation_data.meta:
            observation_data.meta = {}
        
        observation_dict = observation_data.model_dump(exclude_none=True)
        observation_dict['meta'] = observation_dict.get('meta', {})
        observation_dict['meta']['versionId'] = '1'
        observation_dict['meta']['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Extrai patient_id da referência subject
        patient_id = None
        subject_reference = None
        if observation_data.subject and observation_data.subject.reference:
            subject_reference = observation_data.subject.reference
            if subject_reference.startswith("Patient/"):
                patient_id = subject_reference.split("/", 1)[1]
                
                # Verifica se o paciente existe
                patient_exists = db.query(Patient).filter(Patient.id == patient_id).first()
                if not patient_exists:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Referenced patient {subject_reference} does not exist"
                    )
        
        # Extrai valores para colunas específicas
        db_observation = Observation(
            id=observation_data.id,
            identifier=observation_dict.get('identifier'),
            status=observation_dict.get('status'),
            category=observation_dict.get('category'),
            code=observation_dict.get('code'),
            subject_reference=subject_reference,
            patient_id=patient_id,
            effective_datetime=observation_dict.get('effectiveDateTime'),
            effective_period=observation_dict.get('effectivePeriod'),
            issued=observation_dict.get('issued'),
            value_quantity=observation_dict.get('valueQuantity'),
            value_codeable_concept=observation_dict.get('valueCodeableConcept'),
            value_string=observation_dict.get('valueString'),
            value_boolean=str(observation_dict.get('valueBoolean', '')).lower() if observation_dict.get('valueBoolean') is not None else None,
            value_integer=observation_dict.get('valueInteger'),
            value_range=observation_dict.get('valueRange'),
            value_ratio=observation_dict.get('valueRatio'),
            value_sampled_data=observation_dict.get('valueSampledData'),
            value_time=observation_dict.get('valueTime'),
            value_datetime=observation_dict.get('valueDateTime'),
            value_period=observation_dict.get('valuePeriod'),
            interpretation=observation_dict.get('interpretation'),
            note=observation_dict.get('note'),
            meta=observation_dict['meta'],
            resource_json=observation_dict
        )
        
        try:
            db.add(db_observation)
            db.commit()
            db.refresh(db_observation)
            return db_observation
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=409, 
                detail=f"Observation with id {observation_data.id} already exists"
            )
    
    @staticmethod
    def get_observation(db: Session, observation_id: str) -> Optional[Observation]:
        """
        Busca uma Observation por ID
        """
        observation = db.query(Observation).filter(Observation.id == observation_id).first()
        if not observation:
            raise HTTPException(status_code=404, detail=f"Observation/{observation_id} not found")
        return observation
    
    @staticmethod
    def search_observations(db: Session, 
                          patient: Optional[str] = None,
                          status: Optional[str] = None,
                          date: Optional[str] = None,
                          limit: int = 50) -> list[Observation]:
        """
        Busca Observations com filtros
        """
        query = db.query(Observation)
        
        if patient:
            # Aceita "Patient/123" ou apenas "123"
            if not patient.startswith("Patient/"):
                patient = f"Patient/{patient}"
            query = query.filter(Observation.subject_reference == patient)
        
        if status:
            query = query.filter(Observation.status == status)
        
        if date:
            query = query.filter(Observation.effective_datetime.like(f"{date}%"))
        
        return query.limit(limit).all()
