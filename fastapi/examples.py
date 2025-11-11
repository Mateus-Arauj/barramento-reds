"""
Exemplos de uso do Mini HAPI via Python
Demonstra como interagir com a API usando a biblioteca requests
"""
import requests
import json
from datetime import datetime
import os

               
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
API_TOKEN = os.getenv("API_TOKEN", "troque-essa-chave")

                
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}


class MiniHAPIClient:
    """Cliente Python para o Mini HAPI"""
    
    def __init__(self, base_url: str = BASE_URL, token: str = API_TOKEN):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    
    def health_check(self):
        """Verifica o status do servidor"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_metadata(self):
        """Retorna o CapabilityStatement"""
        response = requests.get(f"{self.base_url}/metadata")
        return response.json()
    
                                                       
    
    def create_patient(self, patient_data: dict):
        """Cria um novo Patient"""
        response = requests.post(
            f"{self.base_url}/fhir/Patient",
            headers=self.headers,
            json=patient_data
        )
        response.raise_for_status()
        return response.json()
    
    def get_patient(self, patient_id: str):
        """Busca um Patient por ID"""
        response = requests.get(
            f"{self.base_url}/fhir/Patient/{patient_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def update_patient(self, patient_id: str, patient_data: dict):
        """Atualiza um Patient"""
        response = requests.put(
            f"{self.base_url}/fhir/Patient/{patient_id}",
            headers=self.headers,
            json=patient_data
        )
        response.raise_for_status()
        return response.json()
    
    def delete_patient(self, patient_id: str):
        """Deleta um Patient"""
        response = requests.delete(
            f"{self.base_url}/fhir/Patient/{patient_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.status_code == 204
    
    def search_patients(self, name=None, gender=None, birthdate=None, count=50):
        """Busca Patients com filtros"""
        params = {"_count": count}
        if name:
            params["name"] = name
        if gender:
            params["gender"] = gender
        if birthdate:
            params["birthdate"] = birthdate
        
        response = requests.get(
            f"{self.base_url}/fhir/Patient",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    
                                                           
    
    def create_observation(self, observation_data: dict):
        """Cria uma nova Observation"""
        response = requests.post(
            f"{self.base_url}/fhir/Observation",
            headers=self.headers,
            json=observation_data
        )
        response.raise_for_status()
        return response.json()
    
    def get_observation(self, observation_id: str):
        """Busca uma Observation por ID"""
        response = requests.get(
            f"{self.base_url}/fhir/Observation/{observation_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def search_observations(self, patient=None, status=None, date=None, count=50):
        """Busca Observations com filtros"""
        params = {"_count": count}
        if patient:
            params["patient"] = patient
        if status:
            params["status"] = status
        if date:
            params["date"] = date
        
        response = requests.get(
            f"{self.base_url}/fhir/Observation",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()


def exemplo_completo():
    """Exemplo completo de uso do Mini HAPI"""
    
    print("🚀 Iniciando exemplo de uso do Mini HAPI\n")
    
                          
    client = MiniHAPIClient()
    
                     
    print("1. Verificando saúde do servidor...")
    health = client.health_check()
    print(f"   Status: {health['status']}\n")
    
                          
    print("2. Criando um paciente...")
    patient_data = {
        "resourceType": "Patient",
        "identifier": [
            {
                "system": "http://hospital.example.org/patients",
                "value": f"EXEMPLO-{datetime.now().timestamp()}"
            }
        ],
        "active": True,
        "name": [
            {
                "use": "official",
                "family": "Santos",
                "given": ["Maria", "Clara"]
            }
        ],
        "gender": "female",
        "birthDate": "1985-03-20",
        "telecom": [
            {
                "system": "phone",
                "value": "(11) 91234-5678",
                "use": "mobile"
            },
            {
                "system": "email",
                "value": "maria.santos@example.com",
                "use": "home"
            }
        ],
        "address": [
            {
                "use": "home",
                "type": "physical",
                "line": ["Av. Paulista, 1000"],
                "city": "São Paulo",
                "state": "SP",
                "postalCode": "01310-100",
                "country": "BR"
            }
        ]
    }
    
    patient = client.create_patient(patient_data)
    patient_id = patient["id"]
    print(f"   ✓ Paciente criado: {patient_id}")
    print(f"   Nome: {patient['name'][0]['given'][0]} {patient['name'][0]['family']}\n")
    
                          
    print("3. Buscando o paciente...")
    found_patient = client.get_patient(patient_id)
    print(f"   ✓ Paciente encontrado: {found_patient['id']}")
    print(f"   Versão: {found_patient['meta']['versionId']}\n")
    
                                             
    print("4. Criando observação de pressão arterial...")
    observation_pa = {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "85354-9",
                    "display": "Blood pressure panel with all children optional"
                }
            ],
            "text": "Pressão Arterial"
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": "Maria Clara Santos"
        },
        "effectiveDateTime": datetime.now().isoformat() + "Z",
        "valueQuantity": {
            "value": 120,
            "unit": "mmHg",
            "system": "http://unitsofmeasure.org",
            "code": "mm[Hg]"
        },
        "interpretation": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                        "code": "N",
                        "display": "Normal"
                    }
                ]
            }
        ],
        "note": [
            {
                "text": "Pressão arterial dentro dos parâmetros normais"
            }
        ]
    }
    
    obs1 = client.create_observation(observation_pa)
    print(f"   ✓ Observação criada: {obs1['id']}")
    print(f"   Código: {obs1['code']['text']}")
    print(f"   Valor: {obs1['valueQuantity']['value']} {obs1['valueQuantity']['unit']}\n")
    
                                        
    print("5. Criando observação de temperatura...")
    observation_temp = {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "8310-5",
                    "display": "Body temperature"
                }
            ],
            "text": "Temperatura Corporal"
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "effectiveDateTime": datetime.now().isoformat() + "Z",
        "valueQuantity": {
            "value": 36.5,
            "unit": "Cel",
            "system": "http://unitsofmeasure.org",
            "code": "Cel"
        }
    }
    
    obs2 = client.create_observation(observation_temp)
    print(f"   ✓ Observação criada: {obs2['id']}")
    print(f"   Código: {obs2['code']['text']}")
    print(f"   Valor: {obs2['valueQuantity']['value']} {obs2['valueQuantity']['unit']}\n")
    
                                                
    print("6. Buscando observações do paciente...")
    observations_bundle = client.search_observations(patient=patient_id)
    print(f"   ✓ Total de observações: {observations_bundle['total']}")
    for entry in observations_bundle['entry']:
        obs = entry['resource']
        print(f"   - {obs['code']['text']}: {obs.get('valueQuantity', {}).get('value', 'N/A')}")
    print()
    
                                  
    print("7. Buscando pacientes chamados Santos...")
    patients_bundle = client.search_patients(name="Santos")
    print(f"   ✓ Total de pacientes encontrados: {patients_bundle['total']}\n")
    
                           
    print("8. Atualizando dados do paciente...")
    patient_data["active"] = False
    patient_data["telecom"].append({
        "system": "phone",
        "value": "(11) 3456-7890",
        "use": "work"
    })
    
    updated_patient = client.update_patient(patient_id, patient_data)
    print(f"   ✓ Paciente atualizado")
    print(f"   Nova versão: {updated_patient['meta']['versionId']}")
    print(f"   Ativo: {updated_patient['active']}")
    print(f"   Total de telecoms: {len(updated_patient['telecom'])}\n")
    
                         
    print("9. Deletando paciente...")
    deleted = client.delete_patient(patient_id)
    if deleted:
        print(f"   ✓ Paciente deletado com sucesso\n")
    
                                         
    print("10. Tentando buscar paciente deletado...")
    try:
        client.get_patient(patient_id)
        print("   ✗ Erro: paciente ainda existe!\n")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("   ✓ Paciente não encontrado (esperado após deleção)\n")
    
    print("✅ Exemplo concluído com sucesso!")


def exemplo_bulk_observations():
    """Exemplo de criação em massa de observações"""
    
    print("📊 Criando múltiplas observações para um paciente\n")
    
    client = MiniHAPIClient()
    
                    
    patient = client.create_patient({
        "resourceType": "Patient",
        "name": [{"family": "Teste", "given": ["Bulk"]}],
        "gender": "other",
        "birthDate": "2000-01-01"
    })
    patient_id = patient["id"]
    print(f"Paciente criado: {patient_id}\n")
    
                              
    observation_types = [
        ("85354-9", "Pressão Arterial", 120, "mmHg"),
        ("8310-5", "Temperatura", 36.5, "Cel"),
        ("8867-4", "Frequência Cardíaca", 75, "bpm"),
        ("9279-1", "Frequência Respiratória", 16, "rpm"),
        ("2339-0", "Glicose", 95, "mg/dL"),
    ]
    
    for code, display, value, unit in observation_types:
        obs = client.create_observation({
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": code,
                    "display": display
                }],
                "text": display
            },
            "subject": {"reference": f"Patient/{patient_id}"},
            "effectiveDateTime": datetime.now().isoformat() + "Z",
            "valueQuantity": {
                "value": value,
                "unit": unit,
                "system": "http://unitsofmeasure.org"
            }
        })
        print(f"✓ {display}: {value} {unit}")
    
    print(f"\n✅ {len(observation_types)} observações criadas!")
    
                  
    bundle = client.search_observations(patient=patient_id)
    print(f"\nTotal no servidor: {bundle['total']}")


if __name__ == "__main__":
    print("=" * 60)
    print("Mini HAPI - Exemplos de Uso em Python")
    print("=" * 60)
    print()
    
    try:
                                   
        exemplo_completo()
        
        print("\n" + "=" * 60)
        print()
        
                               
        exemplo_bulk_observations()
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor")
        print("   Verifique se o Mini HAPI está rodando em", BASE_URL)
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP: {e}")
        print(f"   Resposta: {e.response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
