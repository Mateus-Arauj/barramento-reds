# Arquitetura Completa do Sistema - TCC

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          BARRAMENTO DE SAÚDE - ARQUITETURA TCC                       │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   📊 FONTE      │───>│  🔄 ETL         │───>│  💾 REPOSITÓRIO │───>│  📈 CONSUMO     │
│   DE DADOS      │    │  (CONECTOR)     │    │  CENTRAL        │    │  DE DADOS       │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Componentes Detalhados

### 1️⃣ SIMULADOR - Fonte de Dados Legada

```
┌─────────────────────────────────────────────────┐
│          🏥 Sistema Legado (Simulado)           │
├─────────────────────────────────────────────────┤
│                                                 │
│  Arquivo: simulator/legacy_system.py            │
│                                                 │
│  Função: Simular Oracle Soul MV                 │
│                                                 │
│  Saídas:                                        │
│  • data/patients_legacy.json                    │
│  • data/exams_legacy.json                       │
│                                                 │
│  Formato: Proprietário (não-FHIR)              │
│  • PACIENTE_ID, NOME_COMPLETO                   │
│  • DATA_NASCIMENTO (DD/MM/YYYY)                 │
│  • SEXO (M/F)                                   │
│  • EXAME_ID, CODIGO_EXAME                       │
│  • VALOR_RESULTADO, STATUS_RESULTADO            │
│                                                 │
└─────────────────────────────────────────────────┘
          │
          │ Dados Legados (JSON)
          ↓
```

### 2️⃣ CONECTOR ETL - Transformação

```
┌─────────────────────────────────────────────────┐
│         🔄 Conector/Adaptador ETL               │
├─────────────────────────────────────────────────┤
│                                                 │
│  Arquivo: connector/fhir_connector.py           │
│                                                 │
│  Função: Extract → Transform → Load             │
│                                                 │
│  EXTRACT:                                       │
│  • Lê patients_legacy.json                      │
│  • Lê exams_legacy.json                         │
│                                                 │
│  TRANSFORM:                                     │
│  • Legado → FHIR Patient                        │
│    ├─ SEXO (M/F) → gender (male/female)        │
│    ├─ DATA_NASCIMENTO → birthDate (ISO)        │
│    ├─ NOME_COMPLETO → name (HumanName)         │
│    └─ STATUS_ATIVO → active (boolean)          │
│                                                 │
│  • Legado → FHIR Observation                    │
│    ├─ CODIGO_EXAME → code (CodeableConcept)    │
│    ├─ VALOR_RESULTADO → valueQuantity          │
│    ├─ STATUS_RESULTADO → interpretation        │
│    └─ PACIENTE_ID → subject.reference          │
│                                                 │
│  LOAD:                                          │
│  • POST /fhir/Patient                           │
│  • POST /fhir/Observation                       │
│                                                 │
└─────────────────────────────────────────────────┘
          │
          │ Recursos FHIR (JSON)
          │ via HTTP POST
          ↓
```

### 3️⃣ MINI HAPI - Repositório Central

```
┌─────────────────────────────────────────────────────────────────┐
│                   💾 Mini HAPI - Servidor FHIR                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Container: fastapi                                             │
│  Porta: 8000                                                    │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  📡 API REST (FastAPI)                                     │ │
│  │  ─────────────────────────────────────────────────────    │ │
│  │                                                            │ │
│  │  app.py - Endpoints FHIR:                                 │ │
│  │  • POST   /fhir/Patient                                   │ │
│  │  • GET    /fhir/Patient/{id}                              │ │
│  │  • PUT    /fhir/Patient/{id}                              │ │
│  │  • DELETE /fhir/Patient/{id}                              │ │
│  │  • GET    /fhir/Patient?filters                           │ │
│  │                                                            │ │
│  │  • POST   /fhir/Observation                               │ │
│  │  • GET    /fhir/Observation/{id}                          │ │
│  │  • GET    /fhir/Observation?filters                       │ │
│  │                                                            │ │
│  │  • GET    /metadata (CapabilityStatement)                 │ │
│  │  • GET    /health                                         │ │
│  │                                                            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                            │                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  🔐 Autenticação                                          │ │
│  │  ───────────────                                          │ │
│  │  Bearer Token (API_TOKEN)                                 │ │
│  └───────────────────────────────────────────────────────────┘ │
│                            │                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  ✅ Validação (Pydantic)                                  │ │
│  │  ────────────────────────                                 │ │
│  │  validators.py - Schemas FHIR:                            │ │
│  │  • PatientResource                                        │ │
│  │  • ObservationResource                                    │ │
│  │  • CodeableConcept, Quantity, etc.                        │ │
│  └───────────────────────────────────────────────────────────┘ │
│                            │                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  💼 Lógica de Negócio (Services)                          │ │
│  │  ───────────────────────────────                          │ │
│  │  services.py:                                             │ │
│  │  • PatientService (CRUD)                                  │ │
│  │  • ObservationService (CRUD)                              │ │
│  │  • Validações de referências                             │ │
│  │  • Metadados FHIR (versionId, lastUpdated)               │ │
│  └───────────────────────────────────────────────────────────┘ │
│                            │                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  🗃️ ORM (SQLAlchemy)                                      │ │
│  │  ─────────────────────                                    │ │
│  │  models.py:                                               │ │
│  │  • Patient (model)                                        │ │
│  │  • Observation (model)                                    │ │
│  │  • Relationships                                          │ │
│  └───────────────────────────────────────────────────────────┘ │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    🗄️ PostgreSQL                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Container: postgres                                            │
│  Database: fhir_db                                              │
│                                                                 │
│  Tabelas:                                                       │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  patients                                              │    │
│  │  ─────────────────────────────────────────────────     │    │
│  │  • id (PK, VARCHAR)                                    │    │
│  │  • resource_json (JSON) - Recurso FHIR completo       │    │
│  │  • name (JSON)           - Array de HumanName         │    │
│  │  • gender (VARCHAR)      - Indexado para busca        │    │
│  │  • birth_date (VARCHAR)  - Indexado                   │    │
│  │  • identifier (JSON)                                   │    │
│  │  • meta (JSON)           - versionId, lastUpdated     │    │
│  │  • created_at, updated_at                              │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  observations                                          │    │
│  │  ─────────────────────────────────────────────────     │    │
│  │  • id (PK, VARCHAR)                                    │    │
│  │  • patient_id (FK → patients.id)                      │    │
│  │  • resource_json (JSON)                                │    │
│  │  • status (VARCHAR)                                    │    │
│  │  • code (JSON)                                         │    │
│  │  • value_quantity (JSON)                               │    │
│  │  • effective_datetime (VARCHAR)                        │    │
│  │  • meta (JSON)                                         │    │
│  │  • created_at, updated_at                              │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Relação: patients 1───────∞ observations                      │
│                    └──┤ ON DELETE CASCADE                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ SQL Queries
                             │ (via API REST)
                             ↓
```

### 4️⃣ VISUALIZAÇÃO - Consumo de Dados

```
┌─────────────────────────────────────────────────┐
│         📈 Visualização (Jupyter)               │
├─────────────────────────────────────────────────┤
│                                                 │
│  Arquivo: visualization/                        │
│          fhir_visualization.ipynb               │
│                                                 │
│  Consultas via HTTP:                            │
│  • GET /fhir/Patient                            │
│  • GET /fhir/Observation?patient={id}           │
│                                                 │
│  Processamento:                                 │
│  • pandas DataFrames                            │
│  • Análise estatística                          │
│  • Agregações                                   │
│                                                 │
│  Visualizações:                                 │
│  • Distribuição por gênero (pie chart)          │
│  • Status dos pacientes (bar chart)             │
│  • Tipos de exames (horizontal bar)             │
│  • Tabelas formatadas                           │
│                                                 │
│  Bibliotecas:                                   │
│  • matplotlib, seaborn                          │
│  • pandas                                       │
│  • requests                                     │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Fluxo de Dados Completo

```
1. GERAÇÃO
   └─> legacy_system.py
       └─> data/patients_legacy.json
       └─> data/exams_legacy.json

2. TRANSFORMAÇÃO
   └─> fhir_connector.py
       ├─> Lê JSON legado
       ├─> Transforma para FHIR
       └─> POST para Mini HAPI

3. ARMAZENAMENTO
   └─> Mini HAPI recebe
       ├─> Valida (Pydantic)
       ├─> Processa (Services)
       └─> Persiste (PostgreSQL)

4. CONSUMO
   └─> Jupyter Notebook
       ├─> GET da API FHIR
       ├─> Processa (pandas)
       └─> Visualiza (matplotlib)
```

## Padrões e Tecnologias

| Camada       | Tecnologia             | Padrão            |
| ------------ | ---------------------- | ----------------- |
| Simulador    | Python 3.12            | JSON              |
| Conector     | Python 3.12 + requests | ETL               |
| API          | FastAPI                | REST, FHIR R4     |
| Validação    | Pydantic               | Schema Validation |
| ORM          | SQLAlchemy             | Active Record     |
| Banco        | PostgreSQL 16          | Relacional + JSON |
| Visualização | Jupyter + pandas       | Notebook          |

## Benefícios da Arquitetura

✅ **Modular**: Cada componente pode ser desenvolvido/testado independentemente
✅ **Extensível**: Fácil adicionar novos recursos FHIR
✅ **Escalável**: PostgreSQL + FastAPI suportam alto volume
✅ **Educacional**: Código claro e bem documentado para TCC
✅ **Padrões**: Segue HL7 FHIR R4
✅ **Python Puro**: Stack unificado, fácil manutenção

## Comparação com REDS-PE

| Aspecto       | REDS-PE               | Este TCC            |
| ------------- | --------------------- | ------------------- |
| Fonte         | Oracle Soul MV        | Simulador Python    |
| ETL           | Airflow + Java/Python | Python puro         |
| Servidor FHIR | HAPI (Java)           | Mini HAPI (Python)  |
| Banco         | PostgreSQL            | PostgreSQL          |
| Visualização  | Frontend complexo     | Jupyter Notebook    |
| Complexidade  | Alta                  | Média (educacional) |
| Recursos FHIR | ~150                  | 2 (extensível)      |
| Memória       | ~4GB                  | ~200MB              |

---

**Esta arquitetura demonstra um barramento de saúde completo e funcional,
adequado para fins acadêmicos (TCC) e entendimento profundo da especificação FHIR.**
