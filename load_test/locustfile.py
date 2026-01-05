"""
Teste de Carga - Mini HAPI FHIR Server
Simula múltiplos usuários criando e consultando pacientes e observações
"""
from locust import HttpUser, task, between
import json
import random
from datetime import datetime, timedelta


class FHIRUser(HttpUser):
    """
    Simula um usuário interagindo com o servidor FHIR
    """
    wait_time = between(1, 3)  # Espera entre 1-3 segundos entre requisições
    
    def on_start(self):
        """
        Executado quando um usuário inicia
        Configura headers de autenticação
        """
        self.headers = {
            "Content-Type": "application/fhir+json",
            "Authorization": "Bearer test-token"  # Ajustar conforme seu .env
        }
        self.patient_ids = []
        self.observation_ids = []
    
    def generate_patient_data(self):
        """Gera dados fictícios de paciente FHIR"""
        first_names = ["João", "Maria", "Pedro", "Ana", "Carlos", "Julia", "Lucas", "Beatriz"]
        last_names = ["Silva", "Santos", "Oliveira", "Souza", "Costa", "Ferreira", "Rodrigues"]
        
        return {
            "resourceType": "Patient",
            "identifier": [{
                "system": "http://hospital.example.com/patient-id",
                "value": f"LOAD-TEST-{random.randint(100000, 999999)}"
            }],
            "name": [{
                "use": "official",
                "family": random.choice(last_names),
                "given": [random.choice(first_names)]
            }],
            "gender": random.choice(["male", "female"]),
            "birthDate": (datetime.now() - timedelta(days=random.randint(7300, 29200))).strftime("%Y-%m-%d"),
            "telecom": [{
                "system": "phone",
                "value": f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                "use": "mobile"
            }]
        }
    
    def generate_observation_data(self, patient_id):
        """Gera dados fictícios de observação FHIR"""
        observation_types = [
            ("85354-9", "Blood pressure", "mmHg", lambda: random.randint(110, 140)),
            ("8867-4", "Heart rate", "beats/min", lambda: random.randint(60, 100)),
            ("8310-5", "Body temperature", "Cel", lambda: round(random.uniform(36.0, 37.5), 1)),
            ("2339-0", "Glucose", "mg/dL", lambda: random.randint(70, 120))
        ]
        
        code, display, unit, value_generator = random.choice(observation_types)
        
        return {
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": code,
                    "display": display
                }]
            },
            "subject": {
                "reference": f"Patient/{patient_id}"
            },
            "effectiveDateTime": datetime.now().isoformat(),
            "valueQuantity": {
                "value": value_generator(),
                "unit": unit,
                "system": "http://unitsofmeasure.org",
                "code": unit
            }
        }
    
    @task(3)
    def create_patient(self):
        """
        Task: Criar um novo paciente
        Peso: 3 (executado com mais frequência)
        """
        patient_data = self.generate_patient_data()
        
        with self.client.post(
            "/fhir/Patient",
            json=patient_data,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 201:
                try:
                    patient_id = response.json().get("id")
                    if patient_id:
                        self.patient_ids.append(patient_id)
                    response.success()
                except:
                    response.failure("Failed to parse patient ID")
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(2)
    def get_patient(self):
        """
        Task: Buscar um paciente existente
        Peso: 2
        """
        if not self.patient_ids:
            return
        
        patient_id = random.choice(self.patient_ids)
        
        with self.client.get(
            f"/fhir/Patient/{patient_id}",
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(2)
    def create_observation(self):
        """
        Task: Criar uma observação para um paciente
        Peso: 2
        """
        if not self.patient_ids:
            # Se não há pacientes, cria um primeiro
            self.create_patient()
            return
        
        patient_id = random.choice(self.patient_ids)
        observation_data = self.generate_observation_data(patient_id)
        
        with self.client.post(
            "/fhir/Observation",
            json=observation_data,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 201:
                try:
                    observation_id = response.json().get("id")
                    if observation_id:
                        self.observation_ids.append(observation_id)
                    response.success()
                except:
                    response.failure("Failed to parse observation ID")
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(1)
    def get_observation(self):
        """
        Task: Buscar uma observação existente
        Peso: 1
        """
        if not self.observation_ids:
            return
        
        observation_id = random.choice(self.observation_ids)
        
        with self.client.get(
            f"/fhir/Observation/{observation_id}",
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(1)
    def search_patients(self):
        """
        Task: Buscar pacientes com filtros
        Peso: 1
        """
        search_params = [
            "?gender=male",
            "?gender=female",
            "?_count=10",
            "?family=Silva",
        ]
        
        param = random.choice(search_params)
        
        with self.client.get(
            f"/fhir/Patient{param}",
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
    
    @task(1)
    def health_check(self):
        """
        Task: Verificar saúde do sistema
        Peso: 1
        """
        with self.client.get(
            "/health",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
