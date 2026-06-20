# 🏥 Barramento de Saúde FHIR - TCC

Sistema completo de integração de dados de saúde usando padrão HL7 FHIR, desenvolvido em **Python puro**.

## 📋 Sobre o Projeto

Este projeto implementa um **barramento de interoperabilidade em saúde** completo, demonstrando:

1. **Integração de sistema legado** → Simulador de Oracle Soul MV
2. **Processo ETL** → Conector que transforma dados proprietários em FHIR
3. **Servidor FHIR** → Mini HAPI (FastAPI + PostgreSQL)
4. **Visualização de dados** → Jupyter Notebook com análises

## 🏗️ Arquitetura

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Simulador   │───>│  Conector    │───>│  Mini HAPI   │───>│ Visualização │
│  (Legado)    │    │  ETL         │    │  (Servidor   │    │  (Jupyter)   │
│              │    │  Transform   │    │   FHIR)      │    │              │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
    Python              Python              FastAPI +           pandas +
    JSON                requests            PostgreSQL          matplotlib
```

Veja detalhes em: [ARCHITECTURE.md](ARCHITECTURE.md)

## ✨ Funcionalidades

### Mini HAPI (Servidor FHIR)

- ✅ **POST** `/fhir/Patient` - Criar paciente
- ✅ **GET** `/fhir/Patient/{id}` - Buscar paciente
- ✅ **PUT** `/fhir/Patient/{id}` - Atualizar paciente
- ✅ **DELETE** `/fhir/Patient/{id}` - Deletar paciente
- ✅ **GET** `/fhir/Patient?filters` - Buscar com filtros
- ✅ **POST** `/fhir/Observation` - Criar observação/exame
- ✅ **GET** `/fhir/Observation/{id}` - Buscar observação
- ✅ **GET** `/fhir/Observation?filters` - Buscar com filtros
- ✅ **GET** `/metadata` - CapabilityStatement
- ✅ **GET** `/health` - Health check

### Conector ETL

- ✅ Lê dados de sistema legado (JSON)
- ✅ Transforma para recursos FHIR válidos
- ✅ Envia para Mini HAPI via API REST
- ✅ Estatísticas e logs detalhados

### Simulador

- ✅ Gera pacientes fictícios em formato legado
- ✅ Gera exames/observações associados
- ✅ Simula campos de Oracle Soul MV

### Visualização

- ✅ Jupyter Notebook interativo
- ✅ Consultas via API FHIR
- ✅ Gráficos e análises estatísticas
- ✅ Demonstração ponta a ponta

## 🚀 Quick Start

### Passo 1: Configurar e Iniciar

```bash
# Clonar repositório
git clone <repo-url>
cd mdb-health

# Configurar ambiente
cp .env.example .env
# Edite .env com seu API_TOKEN

# Iniciar infraestrutura
docker-compose up -d

# Verificar
curl http://localhost:8000/health
```

### Passo 2: Gerar Dados Legados

```bash
python3 simulator/legacy_system.py
```

### Passo 3: Executar ETL

```bash
python3 connector/fhir_connector.py
```

### Passo 4: Visualizar

```bash
# Instalar dependências
pip3 install -r visualization/requirements.txt

# Iniciar Jupyter
jupyter notebook

# Abrir: visualization/fhir_visualization.ipynb
```

📖 **Guia completo**: [STEP_BY_STEP.md](STEP_BY_STEP.md)

## 📁 Estrutura do Projeto

```
mdb-health/
├── simulator/              # Simulador de sistema legado
│   ├── legacy_system.py   # Gerador de dados
│   ├── data/              # Dados gerados (JSON)
│   └── README.md
│
├── connector/             # Conector ETL
│   ├── fhir_connector.py # Transformador Legado → FHIR
│   └── README.md
│
├── fastapi/              # Mini HAPI (Servidor FHIR)
│   ├── app.py           # API REST endpoints
│   ├── models.py        # SQLAlchemy models
│   ├── database.py      # Configuração PostgreSQL
│   ├── validators.py    # Schemas Pydantic FHIR
│   ├── services.py      # Lógica de negócio
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── visualization/        # Análise e visualização
│   ├── fhir_visualization.ipynb
│   ├── requirements.txt
│   └── README.md
│
├── postgres/            # Inicialização do banco
│   └── init/
│       └── 01_init.sql
│
├── docker-compose.yml   # Orquestração de serviços
├── .env.example        # Template de configuração
│
├── STEP_BY_STEP.md     # Guia de execução
├── ARCHITECTURE.md     # Arquitetura detalhada
├── TCC_DOCUMENTATION.md # Documentação acadêmica
├── QUICKSTART.md       # Início rápido
└── README.md           # Este arquivo
```

## 🛠️ Tecnologias

| Componente      | Tecnologia       | Versão |
| --------------- | ---------------- | ------ |
| Linguagem       | Python           | 3.12+  |
| API             | FastAPI          | 0.115+ |
| ORM             | SQLAlchemy       | 2.0+   |
| Validação       | Pydantic         | 2.9+   |
| Banco de Dados  | PostgreSQL       | 16     |
| Visualização    | Jupyter + pandas | Latest |
| Containerização | Docker           | Latest |

## 📊 Dados do Sistema

### Exemplo: Patient (FHIR)

```json
{
  "resourceType": "Patient",
  "id": "uuid-gerado",
  "identifier": [
    {
      "system": "http://hospital.example.org/legacy-patient-id",
      "value": "PAC123456"
    }
  ],
  "name": [
    {
      "family": "Silva",
      "given": ["João", "Carlos"]
    }
  ],
  "gender": "male",
  "birthDate": "1980-05-15",
  "active": true
}
```

### Exemplo: Observation (FHIR)

```json
{
  "resourceType": "Observation",
  "id": "uuid-gerado",
  "status": "final",
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "2339-0",
        "display": "Glicemia"
      }
    ],
    "text": "Glicemia em Jejum"
  },
  "subject": {
    "reference": "Patient/uuid-do-paciente"
  },
  "valueQuantity": {
    "value": 95.5,
    "unit": "mg/dL"
  },
  "interpretation": [
    {
      "coding": [
        {
          "code": "N",
          "display": "Normal"
        }
      ]
    }
  ]
}
```

## 🧪 Testes

```bash
# Executar testes automatizados
cd fastapi
chmod +x test_api.sh
./test_api.sh

# Ou usar o menu interativo
./dev-tools.sh
# Opção 7: Executar testes
```

## 📚 Documentação

| Documento                                          | Descrição                     |
| -------------------------------------------------- | ----------------------------- |
| [STEP_BY_STEP.md](STEP_BY_STEP.md)                 | **Guia de execução completo** |
| [ARCHITECTURE.md](ARCHITECTURE.md)                 | Arquitetura detalhada         |
| [TCC_DOCUMENTATION.md](TCC_DOCUMENTATION.md)       | Documentação acadêmica        |
| [QUICKSTART.md](QUICKSTART.md)                     | Início rápido                 |
| [fastapi/README.md](fastapi/README.md)             | Mini HAPI API                 |
| [simulator/README.md](simulator/README.md)         | Simulador                     |
| [connector/README.md](connector/README.md)         | Conector ETL                  |
| [visualization/README.md](visualization/README.md) | Visualização                  |

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
# API
API_TOKEN=seu-token-seguro
FASTAPI_PORT=8000

# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=senha-segura
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
FHIR_DB=fhir_db

# Outros serviços (opcionais)
HAPI_HTTP_PORT=8080
SUPERSET_PORT=8088
```

## 🎯 Casos de Uso

1. **Acadêmico (TCC)**: Demonstração de barramento FHIR completo
2. **Educacional**: Aprendizado de FHIR e interoperabilidade
3. **Prototipagem**: Base para sistemas maiores
4. **Integração**: Conectar sistemas legados a padrões modernos

## 🤝 Contribuindo

Este é um projeto acadêmico, mas sugestões são bem-vindas:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos (TCC).

## 🙏 Agradecimentos

- **HL7 FHIR**: Especificação FHIR R4
- **FastAPI**: Framework web moderno
- **PostgreSQL**: Banco de dados robusto
- **Comunidade Python**: Bibliotecas excelentes

## 📞 Contato

Para dúvidas sobre o TCC ou implementação, consulte a documentação ou abra uma issue.

---

## ⚡ Links Rápidos

- 📖 [Começar agora](STEP_BY_STEP.md)
- 🏗️ [Ver arquitetura](ARCHITECTURE.md)
- 🎓 [Documentação TCC](TCC_DOCUMENTATION.md)
- 📊 [API Docs (Swagger)](http://localhost:8000/docs)
- 💾 [Mini HAPI](fastapi/README.md)

---

**Desenvolvido com ❤️ para demonstrar integração de sistemas de saúde com FHIR**
