#!/usr/bin/env python3
"""
Teste de Carga Simples - Mini HAPI FHIR Server
Roda dentro do container Python sem dependências externas
Usa apenas bibliotecas padrão: threading, requests
"""

import time
import random
import json
import threading
import statistics
from datetime import datetime, timedelta
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict
import sys

try:
    import requests
except ImportError:
    print("❌ requests não encontrado. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


@dataclass
class RequestResult:
    """Resultado de uma requisição"""
    endpoint: str
    method: str
    status_code: int
    response_time: float  # em milissegundos
    success: bool
    timestamp: datetime = field(default_factory=datetime.now)


class LoadTester:
    """Classe principal para teste de carga"""
    
    def __init__(self, base_url: str, token: str, num_users: int, duration: int):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.num_users = num_users
        self.duration = duration  # segundos
        
        self.results: List[RequestResult] = []
        self.results_lock = threading.Lock()
        
        self.patient_ids = []
        self.patient_ids_lock = threading.Lock()
        
        self.observation_ids = []
        self.observation_ids_lock = threading.Lock()
        
        self.start_time = None
        self.stop_flag = threading.Event()
        
        self.headers = {
            "Content-Type": "application/fhir+json",
            "Authorization": f"Bearer {token}"
        }
    
    def add_result(self, result: RequestResult):
        """Adiciona resultado de forma thread-safe"""
        with self.results_lock:
            self.results.append(result)
    
    def add_patient_id(self, patient_id: str):
        """Adiciona ID de paciente de forma thread-safe"""
        with self.patient_ids_lock:
            self.patient_ids.append(patient_id)
    
    def get_random_patient_id(self):
        """Obtém ID de paciente aleatório de forma thread-safe"""
        with self.patient_ids_lock:
            if self.patient_ids:
                return random.choice(self.patient_ids)
        return None
    
    def add_observation_id(self, obs_id: str):
        """Adiciona ID de observação de forma thread-safe"""
        with self.observation_ids_lock:
            self.observation_ids.append(obs_id)
    
    def get_random_observation_id(self):
        """Obtém ID de observação aleatório de forma thread-safe"""
        with self.observation_ids_lock:
            if self.observation_ids:
                return random.choice(self.observation_ids)
        return None
    
    def generate_patient_data(self):
        """Gera dados fictícios de paciente FHIR"""
        first_names = ["João", "Maria", "Pedro", "Ana", "Carlos", "Julia", "Lucas", "Beatriz", 
                       "Fernando", "Camila", "Ricardo", "Patricia", "Rafael", "Amanda"]
        last_names = ["Silva", "Santos", "Oliveira", "Souza", "Costa", "Ferreira", 
                      "Rodrigues", "Almeida", "Pereira", "Lima"]
        
        return {
            "resourceType": "Patient",
            "identifier": [{
                "system": "http://hospital.example.com/patient-id",
                "value": f"LOAD-{random.randint(100000, 999999)}"
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
    
    def generate_observation_data(self, patient_id: str):
        """Gera dados fictícios de observação FHIR"""
        observation_types = [
            ("85354-9", "Blood pressure", "mmHg", lambda: random.randint(110, 140)),
            ("8867-4", "Heart rate", "beats/min", lambda: random.randint(60, 100)),
            ("8310-5", "Body temperature", "Cel", lambda: round(random.uniform(36.0, 37.5), 1)),
            ("2339-0", "Glucose", "mg/dL", lambda: random.randint(70, 120)),
            ("2571-8", "Triglycerides", "mg/dL", lambda: random.randint(50, 150)),
            ("2093-3", "Cholesterol", "mg/dL", lambda: random.randint(120, 200))
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
    
    def make_request(self, method: str, endpoint: str, json_data=None):
        """Faz uma requisição HTTP e registra o resultado"""
        url = f"{self.base_url}{endpoint}"
        start = time.time()
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=json_data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=json_data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=10)
            else:
                return None
            
            response_time = (time.time() - start) * 1000  # em ms
            success = 200 <= response.status_code < 300
            
            result = RequestResult(
                endpoint=endpoint,
                method=method,
                status_code=response.status_code,
                response_time=response_time,
                success=success
            )
            
            self.add_result(result)
            
            return response if success else None
            
        except Exception as e:
            response_time = (time.time() - start) * 1000
            result = RequestResult(
                endpoint=endpoint,
                method=method,
                status_code=0,
                response_time=response_time,
                success=False
            )
            self.add_result(result)
            return None
    
    def user_behavior(self, user_id: int):
        """Simula comportamento de um usuário"""
        print(f"👤 Usuário {user_id} iniciado")
        
        while not self.stop_flag.is_set():
            # Escolhe uma ação aleatória com pesos
            action = random.choices(
                ['create_patient', 'get_patient', 'create_observation', 
                 'get_observation', 'search_patients', 'health'],
                weights=[3, 2, 2, 1, 1, 1]
            )[0]
            
            try:
                if action == 'create_patient':
                    patient_data = self.generate_patient_data()
                    response = self.make_request("POST", "/fhir/Patient", patient_data)
                    if response:
                        try:
                            patient_id = response.json().get("id")
                            if patient_id:
                                self.add_patient_id(patient_id)
                        except:
                            pass
                
                elif action == 'get_patient':
                    patient_id = self.get_random_patient_id()
                    if patient_id:
                        self.make_request("GET", f"/fhir/Patient/{patient_id}")
                
                elif action == 'create_observation':
                    patient_id = self.get_random_patient_id()
                    if patient_id:
                        obs_data = self.generate_observation_data(patient_id)
                        response = self.make_request("POST", "/fhir/Observation", obs_data)
                        if response:
                            try:
                                obs_id = response.json().get("id")
                                if obs_id:
                                    self.add_observation_id(obs_id)
                            except:
                                pass
                
                elif action == 'get_observation':
                    obs_id = self.get_random_observation_id()
                    if obs_id:
                        self.make_request("GET", f"/fhir/Observation/{obs_id}")
                
                elif action == 'search_patients':
                    search_params = ["?gender=male", "?gender=female", "?_count=10"]
                    param = random.choice(search_params)
                    self.make_request("GET", f"/fhir/Patient{param}")
                
                elif action == 'health':
                    self.make_request("GET", "/health")
                
            except Exception as e:
                pass
            
            # Pausa entre 0.5 e 2 segundos
            time.sleep(random.uniform(0.5, 2.0))
        
        print(f"👤 Usuário {user_id} finalizado")
    
    def run(self):
        """Executa o teste de carga"""
        print("=" * 60)
        print("🔥 Teste de Carga - Mini HAPI FHIR Server")
        print("=" * 60)
        print(f"URL: {self.base_url}")
        print(f"Usuários simultâneos: {self.num_users}")
        print(f"Duração: {self.duration}s")
        print("=" * 60)
        print()
        
        # Verifica se o servidor está acessível
        print("Verificando servidor...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✓ Servidor está respondendo")
            else:
                print(f"⚠️  Servidor retornou status {response.status_code}")
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return
        
        print()
        print("Iniciando teste...")
        print()
        
        self.start_time = time.time()
        
        # Cria threads de usuários
        threads = []
        for i in range(self.num_users):
            thread = threading.Thread(target=self.user_behavior, args=(i+1,))
            thread.daemon = True
            threads.append(thread)
            thread.start()
            time.sleep(0.1)  # Pequeno delay entre spawns
        
        # Aguarda a duração do teste
        try:
            time.sleep(self.duration)
        except KeyboardInterrupt:
            print("\n⚠️  Teste interrompido pelo usuário")
        
        # Sinaliza para parar
        print("\nFinalizando usuários...")
        self.stop_flag.set()
        
        # Aguarda threads terminarem
        for thread in threads:
            thread.join(timeout=2)
        
        # Gera relatório
        self.print_report()
    
    def print_report(self):
        """Imprime relatório de resultados"""
        print()
        print("=" * 60)
        print("📊 RESULTADOS DO TESTE")
        print("=" * 60)
        print()
        
        if not self.results:
            print("Nenhum resultado registrado.")
            return
        
        elapsed_time = time.time() - self.start_time
        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r.success)
        failed_requests = total_requests - successful_requests
        
        print(f"Duração total: {elapsed_time:.2f}s")
        print(f"Total de requisições: {total_requests}")
        print(f"Requisições bem-sucedidas: {successful_requests} ({successful_requests/total_requests*100:.1f}%)")
        print(f"Requisições falhas: {failed_requests} ({failed_requests/total_requests*100:.1f}%)")
        print(f"Requisições/segundo (RPS): {total_requests/elapsed_time:.2f}")
        print()
        
        # Agrupa por endpoint
        endpoint_stats = defaultdict(lambda: {"times": [], "successes": 0, "failures": 0})
        
        for result in self.results:
            key = f"{result.method} {result.endpoint}"
            endpoint_stats[key]["times"].append(result.response_time)
            if result.success:
                endpoint_stats[key]["successes"] += 1
            else:
                endpoint_stats[key]["failures"] += 1
        
        # Estatísticas por endpoint
        print("Estatísticas por Endpoint:")
        print("-" * 60)
        print(f"{'Endpoint':<40} {'Reqs':<8} {'Falhas':<8} {'Avg(ms)':<10} {'p95(ms)':<10}")
        print("-" * 60)
        
        for endpoint, stats in sorted(endpoint_stats.items()):
            times = stats["times"]
            successes = stats["successes"]
            failures = stats["failures"]
            total = successes + failures
            
            if times:
                avg_time = statistics.mean(times)
                p95_time = statistics.quantiles(times, n=20)[18] if len(times) > 1 else times[0]
                
                print(f"{endpoint:<40} {total:<8} {failures:<8} {avg_time:<10.2f} {p95_time:<10.2f}")
        
        print("-" * 60)
        print()
        
        # Estatísticas gerais de tempo
        all_times = [r.response_time for r in self.results]
        if all_times:
            print("Tempos de Resposta (ms):")
            print(f"  Mínimo: {min(all_times):.2f}ms")
            print(f"  Médio: {statistics.mean(all_times):.2f}ms")
            print(f"  Mediana: {statistics.median(all_times):.2f}ms")
            print(f"  Máximo: {max(all_times):.2f}ms")
            if len(all_times) > 1:
                p95 = statistics.quantiles(all_times, n=20)[18]
                p99 = statistics.quantiles(all_times, n=100)[98]
                print(f"  P95: {p95:.2f}ms")
                print(f"  P99: {p99:.2f}ms")
        
        print()
        print("✓ Teste concluído!")
        print("=" * 60)


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Teste de Carga para Mini HAPI FHIR Server')
    parser.add_argument('--url', default='http://localhost:8000', 
                        help='URL base do servidor (padrão: http://localhost:8000)')
    parser.add_argument('--token', default='troque-essa-chave',
                        help='Token de autenticação (padrão: troque-essa-chave)')
    parser.add_argument('--users', type=int, default=10,
                        help='Número de usuários simultâneos (padrão: 10)')
    parser.add_argument('--duration', type=int, default=60,
                        help='Duração do teste em segundos (padrão: 60)')
    
    args = parser.parse_args()
    
    tester = LoadTester(
        base_url=args.url,
        token=args.token,
        num_users=args.users,
        duration=args.duration
    )
    
    tester.run()


if __name__ == "__main__":
    main()
