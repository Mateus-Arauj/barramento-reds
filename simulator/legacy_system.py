"""
Simulador de Sistema Legado (Oracle Soul MV)
Gera dados de pacientes e exames em formato proprietário/legado
"""
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
import os


class LegacySystemSimulator:
    """Simula um sistema legado hospitalar gerando dados em formato não-FHIR"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Dados para geração aleatória
        self.first_names_male = ["João", "Pedro", "Carlos", "José", "Paulo", "Lucas", "André", "Fernando", "Rafael", "Marcos"]
        self.first_names_female = ["Maria", "Ana", "Paula", "Juliana", "Carla", "Fernanda", "Beatriz", "Camila", "Letícia", "Gabriela"]
        self.last_names = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Costa"]
        
        self.cities = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Fortaleza", "Recife", "Curitiba", "Porto Alegre"]
        self.states = ["SP", "RJ", "MG", "BA", "CE", "PE", "PR", "RS"]
        
        self.exam_types = [
            {"code": "HEM001", "name": "Hemograma Completo"},
            {"code": "GLI001", "name": "Glicemia em Jejum"},
            {"code": "COL001", "name": "Colesterol Total"},
            {"code": "URE001", "name": "Ureia"},
            {"code": "CRE001", "name": "Creatinina"},
            {"code": "TGO001", "name": "TGO/AST"},
            {"code": "TGP001", "name": "TGP/ALT"},
            {"code": "TSH001", "name": "TSH"},
            {"code": "PAR001", "name": "Pressão Arterial"},
            {"code": "TEM001", "name": "Temperatura Corporal"},
        ]
    
    def generate_patient_id(self) -> str:
        """Gera ID de paciente no formato do sistema legado"""
        return f"PAC{random.randint(100000, 999999)}"
    
    def generate_cpf(self) -> str:
        """Gera CPF aleatório (apenas para simulação)"""
        return f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
    
    def generate_patient(self) -> Dict:
        """
        Gera dados de um paciente em formato legado (não-FHIR)
        Formato similar ao que viria de um Oracle Soul MV
        """
        gender = random.choice(["M", "F"])
        first_name = random.choice(self.first_names_male if gender == "M" else self.first_names_female)
        last_name = random.choice(self.last_names)
        
        birth_year = random.randint(1940, 2010)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        
        patient = {
            # Campos do sistema legado (formato proprietário)
            "PACIENTE_ID": self.generate_patient_id(),
            "NOME_COMPLETO": f"{first_name} {random.choice(self.last_names)} {last_name}",
            "DATA_NASCIMENTO": f"{birth_day:02d}/{birth_month:02d}/{birth_year}",
            "SEXO": gender,  # M/F ao invés de male/female
            "CPF": self.generate_cpf(),
            "PRONTUARIO": f"PRONT-{random.randint(10000, 99999)}",
            
            # Contato
            "TELEFONE_1": f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            "TELEFONE_2": f"(11) 3{random.randint(100, 999)}-{random.randint(1000, 9999)}" if random.random() > 0.5 else None,
            "EMAIL": f"{first_name.lower()}.{last_name.lower()}@email.com",
            
            # Endereço
            "ENDERECO_RUA": f"Rua {random.choice(['das Flores', 'Principal', 'Central', 'do Comércio'])}, {random.randint(1, 999)}",
            "ENDERECO_BAIRRO": random.choice(["Centro", "Jardim América", "Vila Nova", "Parque Industrial"]),
            "ENDERECO_CIDADE": random.choice(self.cities),
            "ENDERECO_ESTADO": random.choice(self.states),
            "ENDERECO_CEP": f"{random.randint(10000, 99999)}-{random.randint(100, 999)}",
            
            # Metadados do sistema legado
            "STATUS_ATIVO": random.choice(["S", "N"]),  # S/N ao invés de true/false
            "DATA_CADASTRO": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "USUARIO_CADASTRO": f"USER{random.randint(1, 50)}",
        }
        
        return patient
    
    def generate_exam_result(self, patient_id: str) -> Dict:
        """
        Gera resultado de exame em formato legado
        """
        exam = random.choice(self.exam_types)
        
        # Valores de referência baseados no tipo de exame
        value_ranges = {
            "HEM001": (12.0, 16.0, "g/dL"),
            "GLI001": (70, 99, "mg/dL"),
            "COL001": (150, 200, "mg/dL"),
            "URE001": (15, 45, "mg/dL"),
            "CRE001": (0.6, 1.2, "mg/dL"),
            "TGO001": (5, 40, "U/L"),
            "TGP001": (7, 56, "U/L"),
            "TSH001": (0.4, 4.0, "mU/L"),
            "PAR001": (110, 130, "mmHg"),
            "TEM001": (36.0, 37.5, "°C"),
        }
        
        min_val, max_val, unit = value_ranges.get(exam["code"], (0, 100, ""))
        value = round(random.uniform(min_val, max_val * 1.2), 2)  # Pode estar fora do normal
        
        exam_date = datetime.now() - timedelta(days=random.randint(0, 30))
        
        result = {
            # Campos do sistema legado
            "EXAME_ID": f"EXM{random.randint(100000, 999999)}",
            "PACIENTE_ID": patient_id,
            "CODIGO_EXAME": exam["code"],
            "NOME_EXAME": exam["name"],
            "VALOR_RESULTADO": value,
            "UNIDADE_MEDIDA": unit,
            "VALOR_REFERENCIA_MIN": min_val,
            "VALOR_REFERENCIA_MAX": max_val,
            "STATUS_RESULTADO": random.choice(["NORMAL", "ALTERADO", "CRITICO"]),
            "DATA_COLETA": exam_date.strftime("%d/%m/%Y %H:%M"),
            "DATA_RESULTADO": (exam_date + timedelta(hours=random.randint(2, 48))).strftime("%d/%m/%Y %H:%M"),
            "MEDICO_SOLICITANTE": f"Dr. {random.choice(self.last_names)}",
            "CRM_MEDICO": f"CRM-SP {random.randint(10000, 99999)}",
            "LABORATORIO": random.choice(["Lab Central", "Lab Norte", "Lab Sul"]),
            "OBSERVACOES": "Resultado dentro do esperado" if random.random() > 0.3 else "Atenção: valor alterado",
        }
        
        return result
    
    def generate_dataset(self, num_patients: int = 100, exams_per_patient: int = 3):
        """
        Gera dataset completo de pacientes e exames
        """
        print(f"🔄 Gerando {num_patients} pacientes...")
        
        patients = []
        exams = []
        
        for i in range(num_patients):
            patient = self.generate_patient()
            patients.append(patient)
            
            # Gera exames para este paciente
            num_exams = random.randint(1, exams_per_patient)
            for _ in range(num_exams):
                exam = self.generate_exam_result(patient["PACIENTE_ID"])
                exams.append(exam)
        
        # Salva em arquivos
        patients_file = os.path.join(self.data_dir, "patients_legacy.json")
        exams_file = os.path.join(self.data_dir, "exams_legacy.json")
        
        with open(patients_file, 'w', encoding='utf-8') as f:
            json.dump(patients, f, ensure_ascii=False, indent=2)
        
        with open(exams_file, 'w', encoding='utf-8') as f:
            json.dump(exams, f, ensure_ascii=False, indent=2)
        
        print(f"✓ {len(patients)} pacientes salvos em {patients_file}")
        print(f"✓ {len(exams)} exames salvos em {exams_file}")
        
        return patients, exams
    
    def get_patients(self) -> List[Dict]:
        """Lê pacientes do arquivo"""
        patients_file = os.path.join(self.data_dir, "patients_legacy.json")
        if os.path.exists(patients_file):
            with open(patients_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def get_exams(self) -> List[Dict]:
        """Lê exames do arquivo"""
        exams_file = os.path.join(self.data_dir, "exams_legacy.json")
        if os.path.exists(exams_file):
            with open(exams_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def get_patient_by_id(self, patient_id: str) -> Dict:
        """Busca paciente específico"""
        patients = self.get_patients()
        for patient in patients:
            if patient["PACIENTE_ID"] == patient_id:
                return patient
        return None
    
    def get_exams_by_patient(self, patient_id: str) -> List[Dict]:
        """Busca exames de um paciente"""
        exams = self.get_exams()
        return [exam for exam in exams if exam["PACIENTE_ID"] == patient_id]


def main():
    """Função principal para executar o simulador"""
    print("=" * 60)
    print("SIMULADOR DE SISTEMA LEGADO - Oracle Soul MV")
    print("=" * 60)
    print()
    
    simulator = LegacySystemSimulator()
    
    # Gera dataset
    patients, exams = simulator.generate_dataset(num_patients=50, exams_per_patient=5)
    
    print()
    print("📊 Exemplo de Paciente (formato legado):")
    print("-" * 60)
    print(json.dumps(patients[0], ensure_ascii=False, indent=2))
    
    print()
    print("📊 Exemplo de Exame (formato legado):")
    print("-" * 60)
    print(json.dumps(exams[0], ensure_ascii=False, indent=2))
    
    print()
    print("=" * 60)
    print("✅ Dataset gerado com sucesso!")
    print("=" * 60)
    print()
    print("Próximo passo: Execute o conector para transformar")
    print("esses dados legados em recursos FHIR e enviá-los")
    print("para o Mini HAPI.")


if __name__ == "__main__":
    main()
