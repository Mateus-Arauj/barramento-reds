# Mini HAPI - Servidor FHIR Simplificado

Este é um servidor FHIR simplificado desenvolvido em Python usando FastAPI e PostgreSQL como parte do TCC. Ele substitui o HAPI FHIR Server (Java) por uma implementação mais leve e customizada.

## 📋 Recursos Implementados

O Mini HAPI implementa os seguintes recursos FHIR R4:

### Patient (Paciente)

- ✅ `POST /fhir/Patient` - Criar paciente
- ✅ `GET /fhir/Patient/{id}` - Buscar paciente por ID
- ✅ `PUT /fhir/Patient/{id}` - Atualizar paciente
- ✅ `DELETE /fhir/Patient/{id}` - Deletar paciente
- ✅ `GET /fhir/Patient?name=...&gender=...&birthdate=...` - Buscar pacientes com filtros

### Observation (Observação)

- ✅ `POST /fhir/Observation` - Criar observação
- ✅ `GET /fhir/Observation/{id}` - Buscar observação por ID
- ✅ `GET /fhir/Observation?patient=...&status=...&date=...` - Buscar observações com filtros

### Metadados

- ✅ `GET /metadata` - CapabilityStatement do servidor
- ✅ `GET /health` - Health check

## 🏗️ Arquitetura

```
fastapi/
├── app.py          # Endpoints FastAPI e rotas
├── models.py       # Modelos SQLAlchemy (Patient, Observation)
├── database.py     # Configuração do banco PostgreSQL
├── validators.py   # Validadores Pydantic para FHIR
├── services.py     # Lógica de negócio
├── requirements.txt
└── Dockerfile
```

### Fluxo de Dados

```
Cliente → FastAPI → Validação (Pydantic) → Serviço → SQLAlchemy → PostgreSQL
                      ↓                        ↓
                  Autenticação            Transformação
                  (Bearer Token)         FHIR ↔ DB
```

## 🚀 Como Usar

### 1. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e ajuste as variáveis:

```bash
cp .env.example .env
```

Principais variáveis:

```env
FHIR_DB=fhir_db
FHIR_DB_USER=fhir_user
FHIR_DB_PASS=fhir_pass
API_TOKEN=seu-token-seguro
```

### 2. Iniciar os Serviços

```bash
docker-compose up -d
```

O Mini HAPI estará disponível em:

- Internamente: `http://fastapi:8000`
- Via nginx-proxy: `https://api.damatlas.cloud`

### 3. Testar a API

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Metadata (CapabilityStatement)

```bash
curl http://localhost:8000/metadata
```

## 📝 Exemplos de Uso

Todos os exemplos abaixo requerem autenticação via Bearer token:

```bash
TOKEN="seu-token-aqui"
```

### Criar um Patient

```bash
curl -X POST http://localhost:8000/fhir/Patient \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "resourceType": "Patient",
    "identifier": [
      {
        "system": "http://hospital.example.org/patients",
        "value": "12345"
      }
    ],
    "active": true,
    "name": [
      {
        "use": "official",
        "family": "Silva",
        "given": ["João", "Carlos"]
      }
    ],
    "gender": "male",
    "birthDate": "1980-05-15",
    "telecom": [
      {
        "system": "phone",
        "value": "(11) 98765-4321",
        "use": "mobile"
      }
    ],
    "address": [
      {
        "use": "home",
        "type": "physical",
        "line": ["Rua das Flores, 123"],
        "city": "São Paulo",
        "state": "SP",
        "postalCode": "01234-567",
        "country": "BR"
      }
    ]
  }'
```

Resposta:

```json
{
  "resourceType": "Patient",
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2024-01-15T10:30:00.000Z"
  },
  "identifier": [
    {
      "system": "http://hospital.example.org/patients",
      "value": "12345"
    }
  ],
  "active": true,
  "name": [
    {
      "use": "official",
      "family": "Silva",
      "given": ["João", "Carlos"]
    }
  ],
  "gender": "male",
  "birthDate": "1980-05-15",
  ...
}
```

### Buscar um Patient

```bash
curl http://localhost:8000/fhir/Patient/a1b2c3d4-e5f6-7890-abcd-ef1234567890 \
  -H "Authorization: Bearer $TOKEN"
```

### Criar uma Observation

```bash
curl -X POST http://localhost:8000/fhir/Observation \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "resourceType": "Observation",
    "status": "final",
    "code": {
      "coding": [
        {
          "system": "http://loinc.org",
          "code": "85354-9",
          "display": "Blood pressure panel"
        }
      ],
      "text": "Pressão Arterial"
    },
    "subject": {
      "reference": "Patient/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    },
    "effectiveDateTime": "2024-01-15T10:30:00Z",
    "valueQuantity": {
      "value": 120,
      "unit": "mmHg",
      "system": "http://unitsofmeasure.org",
      "code": "mm[Hg]"
    },
    "note": [
      {
        "text": "Pressão arterial normal"
      }
    ]
  }'
```

### Buscar Observations de um Patient

```bash
curl "http://localhost:8000/fhir/Observation?patient=a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
  -H "Authorization: Bearer $TOKEN"
```

Resposta (Bundle):

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 1,
  "entry": [
    {
      "fullUrl": "/fhir/Observation/observation-id-123",
      "resource": {
        "resourceType": "Observation",
        "id": "observation-id-123",
        ...
      }
    }
  ]
}
```

### Buscar Patients por Nome

```bash
curl "http://localhost:8000/fhir/Patient?name=Silva&_count=10" \
  -H "Authorization: Bearer $TOKEN"
```

### Atualizar um Patient

```bash
curl -X PUT http://localhost:8000/fhir/Patient/a1b2c3d4-e5f6-7890-abcd-ef1234567890 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "resourceType": "Patient",
    "active": false,
    "name": [
      {
        "use": "official",
        "family": "Silva",
        "given": ["João", "Carlos", "Alberto"]
      }
    ],
    "gender": "male",
    "birthDate": "1980-05-15"
  }'
```

### Deletar um Patient

```bash
curl -X DELETE http://localhost:8000/fhir/Patient/a1b2c3d4-e5f6-7890-abcd-ef1234567890 \
  -H "Authorization: Bearer $TOKEN"
```

## 🔒 Autenticação

O servidor usa autenticação Bearer Token simples. Todas as requisições devem incluir o header:

```
Authorization: Bearer seu-token-aqui
```

O token é configurado via variável de ambiente `API_TOKEN`.

## 🗄️ Banco de Dados

### Estrutura

O PostgreSQL armazena os recursos FHIR em duas tabelas principais:

#### Tabela `patients`

- `id` - UUID do paciente
- `resource_json` - Recurso completo em JSON
- `name`, `gender`, `birth_date` - Campos indexados para busca
- `meta` - Metadados FHIR (versionId, lastUpdated)
- `created_at`, `updated_at` - Timestamps

#### Tabela `observations`

- `id` - UUID da observação
- `resource_json` - Recurso completo em JSON
- `patient_id` - Foreign key para patients
- `status`, `code`, `value_*` - Campos indexados
- `meta` - Metadados FHIR
- `created_at`, `updated_at` - Timestamps

### Migrações

O SQLAlchemy cria as tabelas automaticamente na inicialização:

```python
# Em database.py
init_db()  # Cria todas as tabelas
```

## 🧪 Validação FHIR

O servidor valida os recursos usando Pydantic:

### Patient

- `resourceType` deve ser "Patient"
- `gender` deve ser: male, female, other, unknown
- `birthDate` deve estar no formato YYYY-MM-DD

### Observation

- `resourceType` deve ser "Observation"
- `status` é obrigatório (final, preliminary, etc.)
- `code` é obrigatório (tipo da observação)
- `subject` deve referenciar um Patient existente

Exemplo de erro de validação:

```json
{
  "detail": [
    {
      "loc": ["body", "gender"],
      "msg": "gender must be male, female, other or unknown",
      "type": "value_error"
    }
  ]
}
```

## 📊 Monitoramento

### Logs

```bash
docker-compose logs -f fastapi
```

### Acesso ao Banco

```bash
docker exec -it postgres psql -U postgres -d fhir_db
```

Consultas úteis:

```sql
-- Ver todos os pacientes
SELECT id, name->0->>'family' as family_name, gender, birth_date
FROM patients;

-- Ver todas as observações
SELECT id, status, subject_reference, effective_datetime
FROM observations;

-- Ver observações de um paciente
SELECT o.id, o.status, o.code, o.effective_datetime
FROM observations o
WHERE o.patient_id = 'patient-id-aqui';
```

## 🔧 Desenvolvimento

### Estrutura de Código

#### app.py

- Define endpoints FastAPI
- Gerencia autenticação
- Retorna respostas FHIR

#### models.py

- Modelos SQLAlchemy para ORM
- Define schema do banco de dados
- Relacionamentos entre tabelas

#### validators.py

- Schemas Pydantic para validação
- Modelos FHIR (Patient, Observation)
- Validadores customizados

#### services.py

- Lógica de negócio
- CRUD operations
- Transformação FHIR ↔ Database

#### database.py

- Configuração SQLAlchemy
- Connection pooling
- Session management

### Adicionar Novos Recursos FHIR

1. **Criar modelo** em `models.py`:

```python
class Practitioner(Base):
    __tablename__ = "practitioners"
    id = Column(String(64), primary_key=True)
    resource_json = Column(JSON, nullable=False)
    ...
```

2. **Criar validador** em `validators.py`:

```python
class PractitionerResource(BaseModel):
    resourceType: str = "Practitioner"
    name: Optional[List[HumanName]] = None
    ...
```

3. **Criar serviço** em `services.py`:

```python
class PractitionerService:
    @staticmethod
    def create_practitioner(db, data):
        ...
```

4. **Adicionar endpoints** em `app.py`:

```python
@app.post("/fhir/Practitioner")
async def create_practitioner(...):
    ...
```

## ❓ FAQ

**P: Por que não usar o HAPI FHIR Server?**
R: O Mini HAPI é mais leve, customizável e adequado para TCC, permitindo entender a implementação FHIR em profundidade.

**P: É compatível com FHIR R4?**
R: Sim, implementa um subconjunto do FHIR R4 com Patient e Observation.

**P: Posso adicionar outros recursos FHIR?**
R: Sim! Siga o padrão existente (modelo → validador → serviço → endpoint).

**P: Como fazer backup dos dados?**
R: Use `pg_dump` no container PostgreSQL ou backup do volume Docker.

## 📚 Referências

- [FHIR R4 Specification](https://hl7.org/fhir/R4/)
- [Patient Resource](https://hl7.org/fhir/R4/patient.html)
- [Observation Resource](https://hl7.org/fhir/R4/observation.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
