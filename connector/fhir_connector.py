"""
Conector/Adaptador ETL
Transforma dados do sistema legado em recursos FHIR e envia para o Mini HAPI
"""
import json
import requests
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "simulator"))
print(str(Path(__file__).parent.parent / "simulator"))
from legacy_system import LegacySystemSimulator


class FHIRConnector:
    """
    Conector que transforma dados legados em recursos FHIR
    e os envia para o servidor FHIR (Mini HAPI)
    """
    
    def __init__(self, fhir_base_url: str, api_token: str):
        self.fhir_base_url = fhir_base_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            "Content-Type": "application/fhir+json",
            "Authorization": f"Bearer {api_token}"
        }
        self.stats = {
            "patients_processed": 0,
            "patients_success": 0,
            "patients_failed": 0,
            "observations_processed": 0,
            "observations_success": 0,
            "observations_failed": 0,
        }
    
    def transform_patient_to_fhir(self, legacy_patient: Dict) -> Dict:
        """
        Transforma um paciente do formato legado para FHIR Patient
        
        Mapeamento:
        - PACIENTE_ID -> identifier.value
        - NOME_COMPLETO -> name
        - SEXO (M/F) -> gender (male/female)
        - DATA_NASCIMENTO (DD/MM/YYYY) -> birthDate (YYYY-MM-DD)
        - CPF -> identifier
        - Etc.
        """
                        
        full_name = legacy_patient["NOME_COMPLETO"]
        name_parts = full_name.split()
        given_names = name_parts[:-1]                         
        family_name = name_parts[-1]               
        
                                                     
        birth_date_legacy = legacy_patient["DATA_NASCIMENTO"]
        day, month, year = birth_date_legacy.split('/')
        birth_date_fhir = f"{year}-{month}-{day}"
        
                                            
        gender_map = {"M": "male", "F": "female"}
        gender = gender_map.get(legacy_patient["SEXO"], "unknown")
        
                                                   
        active = legacy_patient["STATUS_ATIVO"] == "S"
        
                                    
        fhir_patient = {
            "resourceType": "Patient",
            "identifier": [
                {
                    "system": "http://hospital.example.org/legacy-patient-id",
                    "value": legacy_patient["PACIENTE_ID"],
                    "use": "official"
                },
                {
                    "system": "http://rnds.saude.gov.br/fhir/r4/NamingSystem/cpf",
                    "value": legacy_patient["CPF"],
                    "use": "official"
                },
                {
                    "system": "http://hospital.example.org/prontuario",
                    "value": legacy_patient["PRONTUARIO"],
                    "use": "usual"
                }
            ],
            "active": active,
            "name": [
                {
                    "use": "official",
                    "family": family_name,
                    "given": given_names,
                    "text": full_name
                }
            ],
            "telecom": [],
            "gender": gender,
            "birthDate": birth_date_fhir,
            "address": [
                {
                    "use": "home",
                    "type": "physical",
                    "line": [legacy_patient["ENDERECO_RUA"]],
                    "city": legacy_patient["ENDERECO_CIDADE"],
                    "state": legacy_patient["ENDERECO_ESTADO"],
                    "postalCode": legacy_patient["ENDERECO_CEP"],
                    "country": "BR",
                    "text": f"{legacy_patient['ENDERECO_RUA']}, {legacy_patient['ENDERECO_BAIRRO']}, {legacy_patient['ENDERECO_CIDADE']}/{legacy_patient['ENDERECO_ESTADO']}"
                }
            ]
        }
        
                           
        if legacy_patient.get("TELEFONE_1"):
            fhir_patient["telecom"].append({
                "system": "phone",
                "value": legacy_patient["TELEFONE_1"],
                "use": "mobile"
            })
        
        if legacy_patient.get("TELEFONE_2"):
            fhir_patient["telecom"].append({
                "system": "phone",
                "value": legacy_patient["TELEFONE_2"],
                "use": "home"
            })
        
        if legacy_patient.get("EMAIL"):
            fhir_patient["telecom"].append({
                "system": "email",
                "value": legacy_patient["EMAIL"],
                "use": "home"
            })
        
        return fhir_patient
    
    def transform_exam_to_fhir(self, legacy_exam: Dict, patient_fhir_id: str) -> Dict:
        """
        Transforma um exame legado em FHIR Observation
        
        Mapeamento:
        - EXAME_ID -> identifier
        - CODIGO_EXAME + NOME_EXAME -> code
        - VALOR_RESULTADO -> valueQuantity
        - STATUS_RESULTADO -> status
        - Etc.
        """
                                                         
        data_coleta = legacy_exam["DATA_COLETA"]
        try:
            dt = datetime.strptime(data_coleta, "%d/%m/%Y %H:%M")
            effective_datetime = dt.isoformat() + "Z"
        except:
            effective_datetime = datetime.now().isoformat() + "Z"
        
                                                   
        status_map = {
            "NORMAL": "final",
            "ALTERADO": "final",
            "CRITICO": "final",
        }
        status = status_map.get(legacy_exam["STATUS_RESULTADO"], "final")
        
                                                   
        interpretation = None
        if legacy_exam["STATUS_RESULTADO"] == "NORMAL":
            interpretation = [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                    "code": "N",
                    "display": "Normal"
                }]
            }]
        elif legacy_exam["STATUS_RESULTADO"] == "ALTERADO":
            interpretation = [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                    "code": "A",
                    "display": "Abnormal"
                }]
            }]
        elif legacy_exam["STATUS_RESULTADO"] == "CRITICO":
            interpretation = [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                    "code": "H",
                    "display": "High"
                }]
            }]
        
                                        
        fhir_observation = {
            "resourceType": "Observation",
            "identifier": [
                {
                    "system": "http://hospital.example.org/legacy-exam-id",
                    "value": legacy_exam["EXAME_ID"]
                }
            ],
            "status": status,
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "laboratory",
                            "display": "Laboratory"
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://hospital.example.org/exam-codes",
                        "code": legacy_exam["CODIGO_EXAME"],
                        "display": legacy_exam["NOME_EXAME"]
                    }
                ],
                "text": legacy_exam["NOME_EXAME"]
            },
            "subject": {
                "reference": f"Patient/{patient_fhir_id}",
                "display": f"Patient ID: {patient_fhir_id}"
            },
            "effectiveDateTime": effective_datetime,
            "valueQuantity": {
                "value": legacy_exam["VALOR_RESULTADO"],
                "unit": legacy_exam["UNIDADE_MEDIDA"],
                "system": "http://unitsofmeasure.org"
            }
        }
        
                                          
        if interpretation:
            fhir_observation["interpretation"] = interpretation
        
                                 
        if legacy_exam.get("VALOR_REFERENCIA_MIN") and legacy_exam.get("VALOR_REFERENCIA_MAX"):
            fhir_observation["referenceRange"] = [
                {
                    "low": {
                        "value": legacy_exam["VALOR_REFERENCIA_MIN"],
                        "unit": legacy_exam["UNIDADE_MEDIDA"]
                    },
                    "high": {
                        "value": legacy_exam["VALOR_REFERENCIA_MAX"],
                        "unit": legacy_exam["UNIDADE_MEDIDA"]
                    }
                }
            ]
        
                                              
        if legacy_exam.get("OBSERVACOES"):
            fhir_observation["note"] = [
                {
                    "text": legacy_exam["OBSERVACOES"]
                }
            ]
        
        return fhir_observation
    
    def send_patient_to_fhir(self, fhir_patient: Dict) -> Optional[str]:
        """
        Envia recurso Patient para o servidor FHIR
        Retorna o ID do paciente se sucesso, None se falha
        """
        try:
            response = requests.post(
                f"{self.fhir_base_url}/fhir/Patient",
                headers=self.headers,
                json=fhir_patient,
                timeout=30
            )
            
            if response.status_code == 201:
                patient_resource = response.json()
                patient_id = patient_resource.get("id")
                self.stats["patients_success"] += 1
                return patient_id
            else:
                print(f"  ✗ Erro ao enviar Patient: HTTP {response.status_code}")
                print(f"    Resposta: {response.text[:200]}")
                self.stats["patients_failed"] += 1
                return None
        
        except Exception as e:
            print(f"  ✗ Exceção ao enviar Patient: {e}")
            self.stats["patients_failed"] += 1
            return None
    
    def send_observation_to_fhir(self, fhir_observation: Dict) -> Optional[str]:
        """
        Envia recurso Observation para o servidor FHIR
        Retorna o ID da observation se sucesso, None se falha
        """
        try:
            response = requests.post(
                f"{self.fhir_base_url}/fhir/Observation",
                headers=self.headers,
                json=fhir_observation,
                timeout=30
            )
            
            if response.status_code == 201:
                observation_resource = response.json()
                observation_id = observation_resource.get("id")
                self.stats["observations_success"] += 1
                return observation_id
            else:
                print(f"  ✗ Erro ao enviar Observation: HTTP {response.status_code}")
                print(f"    Resposta: {response.text[:200]}")
                self.stats["observations_failed"] += 1
                return None
        
        except Exception as e:
            print(f"  ✗ Exceção ao enviar Observation: {e}")
            self.stats["observations_failed"] += 1
            return None
    
    def process_patient(self, legacy_patient: Dict, legacy_exams: List[Dict]) -> bool:
        """
        Processa um paciente completo: transforma e envia paciente + exames
        """
        legacy_id = legacy_patient["PACIENTE_ID"]
        patient_name = legacy_patient["NOME_COMPLETO"]
        
        print(f"\n📋 Processando paciente: {patient_name} ({legacy_id})")
        
                                          
        print("  🔄 Transformando para FHIR Patient...")
        fhir_patient = self.transform_patient_to_fhir(legacy_patient)
        
                                                
        print("  📤 Enviando Patient para Mini HAPI...")
        patient_fhir_id = self.send_patient_to_fhir(fhir_patient)
        
        if not patient_fhir_id:
            print(f"  ✗ Falha ao criar Patient no FHIR")
            return False
        
        print(f"  ✓ Patient criado com ID: {patient_fhir_id}")
        
                                        
        if legacy_exams:
            print(f"  🔄 Processando {len(legacy_exams)} exames...")
            
            for exam in legacy_exams:
                self.stats["observations_processed"] += 1
                
                                                        
                fhir_observation = self.transform_exam_to_fhir(exam, patient_fhir_id)
                
                                   
                obs_id = self.send_observation_to_fhir(fhir_observation)
                
                if obs_id:
                    print(f"    ✓ Observation {exam['NOME_EXAME']}: {obs_id}")
                else:
                    print(f"    ✗ Falha ao criar Observation {exam['NOME_EXAME']}")
        
        return True
    
    def run_etl(self):
        """
        Executa o processo ETL completo:
        1. Extrai dados do sistema legado
        2. Transforma para FHIR
        3. Carrega no Mini HAPI
        """
        print("=" * 70)
        print("CONECTOR ETL - Sistema Legado → FHIR")
        print("=" * 70)
        print()
        
                                             
        simulator = LegacySystemSimulator()
        
                      
        print("📥 EXTRAÇÃO - Lendo dados do sistema legado...")
        patients = simulator.get_patients()
        all_exams = simulator.get_exams()
        
        if not patients:
            print("❌ Nenhum paciente encontrado!")
            print("Execute primeiro: python simulator/legacy_system.py")
            return
        
        print(f"  ✓ {len(patients)} pacientes encontrados")
        print(f"  ✓ {len(all_exams)} exames encontrados")
        
                                
        print()
        print("🔄 TRANSFORMAÇÃO E CARGA - Processando dados...")
        
        for patient in patients:
            self.stats["patients_processed"] += 1
            
                                         
            patient_exams = [
                exam for exam in all_exams 
                if exam["PACIENTE_ID"] == patient["PACIENTE_ID"]
            ]
            
                                             
            self.process_patient(patient, patient_exams)
        
                                   
        print()
        print("=" * 70)
        print("📊 ESTATÍSTICAS FINAIS")
        print("=" * 70)
        print(f"Pacientes processados: {self.stats['patients_processed']}")
        print(f"  ✓ Sucesso: {self.stats['patients_success']}")
        print(f"  ✗ Falhas: {self.stats['patients_failed']}")
        print()
        print(f"Observações processadas: {self.stats['observations_processed']}")
        print(f"  ✓ Sucesso: {self.stats['observations_success']}")
        print(f"  ✗ Falhas: {self.stats['observations_failed']}")
        print("=" * 70)
        
        success_rate = (self.stats['patients_success'] / self.stats['patients_processed'] * 100) if self.stats['patients_processed'] > 0 else 0
        print(f"\n✅ Taxa de sucesso: {success_rate:.1f}%")


def main():
    """Função principal"""
                                                        
    FHIR_BASE_URL = os.getenv("FHIR_BASE_URL", "http://localhost:8000")
    API_TOKEN = os.getenv("API_TOKEN", "troque-essa-chave")
    
                               
    connector = FHIRConnector(FHIR_BASE_URL, API_TOKEN)
    connector.run_etl()


if __name__ == "__main__":
    main()
