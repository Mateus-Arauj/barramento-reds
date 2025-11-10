# 🚀 Guia de Execução Passo a Passo - TCC

Este guia mostra como executar todo o sistema ponta a ponta.

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.12+ instalado
- Git (opcional)

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FLUXO COMPLETO DO TCC                          │
└─────────────────────────────────────────────────────────────────────────┘

1️⃣ SIMULADOR                2️⃣ CONECTOR ETL           3️⃣ MINI HAPI            4️⃣ VISUALIZAÇÃO
   (Sistema Legado)            (Transformação)           (Servidor FHIR)         (Análise)

┌──────────────┐           ┌──────────────┐           ┌──────────────┐       ┌──────────────┐
│  Dados       │           │  Transform   │           │   FastAPI    │       │   Jupyter    │
│  Legados     │  ──────>  │  Legado →    │  ──────>  │   +          │  ───> │   Notebook   │
│  (JSON)      │           │  FHIR        │           │   PostgreSQL │       │              │
└──────────────┘           └──────────────┘           └──────────────┘       └──────────────┘
     Python                     Python                     Python                Python
```

## 🎯 Passo 1: Configurar Ambiente

### 1.1 Configurar Variáveis de Ambiente

```bash
cd /home/nielif/Projetos/mdb-health

# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env (importante!)
nano .env
```

**Variáveis importantes:**

```env
# Token de autenticação (MUDE ESTE VALOR!)
API_TOKEN=seu-token-super-seguro-aqui

# Banco de dados FHIR
FHIR_DB=fhir_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua-senha-postgres
```

### 1.2 Iniciar Infraestrutura

```bash
# Subir todos os serviços
docker-compose up -d

# Verificar se estão rodando
docker-compose ps

# Ver logs do FastAPI
docker-compose logs -f fastapi
```

Aguarde até ver:

```
✓ Tabelas criadas com sucesso
🚀 Uvicorn running on http://0.0.0.0:8000
```

### 1.3 Testar Mini HAPI

```bash
# Health check
curl http://localhost:8000/health

# Deve retornar: {"status":"ok","service":"Mini HAPI FHIR Server"}
```

## 🎯 Passo 2: Gerar Dados Legados

O simulador cria dados fictícios que representam um sistema hospitalar legado.

```bash
# Executar simulador
python3 simulator/legacy_system.py
```

**Saída esperada:**

```
==============================================================
SIMULADOR DE SISTEMA LEGADO - Oracle Soul MV
==============================================================

🔄 Gerando 50 pacientes...
✓ 50 pacientes salvos em simulator/data/patients_legacy.json
✓ 250 exames salvos em simulator/data/exams_legacy.json

📊 Exemplo de Paciente (formato legado):
{
  "PACIENTE_ID": "PAC123456",
  "NOME_COMPLETO": "João Silva Santos",
  "SEXO": "M",
  "DATA_NASCIMENTO": "15/05/1980",
  ...
}
```

**Arquivos gerados:**

- `simulator/data/patients_legacy.json` - Pacientes em formato legado
- `simulator/data/exams_legacy.json` - Exames em formato legado

## 🎯 Passo 3: Executar ETL (Conector)

O conector transforma dados legados em FHIR e os envia para o Mini HAPI.

```bash
# Executar conector
python3 connector/fhir_connector.py
```

**Saída esperada:**

```
======================================================================
CONECTOR ETL - Sistema Legado → FHIR
======================================================================

📥 EXTRAÇÃO - Lendo dados do sistema legado...
  ✓ 50 pacientes encontrados
  ✓ 250 exames encontrados

🔄 TRANSFORMAÇÃO E CARGA - Processando dados...

📋 Processando paciente: João Silva Santos (PAC123456)
  🔄 Transformando para FHIR Patient...
  📤 Enviando Patient para Mini HAPI...
  ✓ Patient criado com ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  🔄 Processando 5 exames...
    ✓ Observation Glicemia em Jejum: obs-123
    ✓ Observation Hemograma Completo: obs-456
    ...

======================================================================
📊 ESTATÍSTICAS FINAIS
======================================================================
Pacientes processados: 50
  ✓ Sucesso: 50
  ✗ Falhas: 0

Observações processadas: 250
  ✓ Sucesso: 250
  ✗ Falhas: 0
======================================================================

✅ Taxa de sucesso: 100.0%
```

## 🎯 Passo 4: Verificar Dados no Mini HAPI

### 4.1 Via cURL

```bash
# Definir token
export TOKEN="seu-token-aqui"

# Buscar pacientes
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/fhir/Patient?_count=5 | jq .

# Buscar observações
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/fhir/Observation?_count=5 | jq .
```

### 4.2 Via Swagger UI

Abra no navegador: http://localhost:8000/docs

- Clique em "Authorize"
- Digite: `Bearer seu-token-aqui`
- Teste os endpoints interativamente

### 4.3 Via Banco de Dados

```bash
# Conectar ao PostgreSQL
docker exec -it postgres psql -U postgres -d fhir_db

# Consultas SQL
SELECT COUNT(*) FROM patients;
SELECT COUNT(*) FROM observations;

SELECT id, name->0->>'text' as nome, gender FROM patients LIMIT 5;

\q  # Sair
```

## 🎯 Passo 5: Visualizar Dados (Jupyter)

### 5.1 Instalar Dependências

```bash
# Instalar bibliotecas necessárias
pip3 install -r visualization/requirements.txt
```

### 5.2 Iniciar Jupyter

```bash
# Opção 1: Jupyter Notebook
jupyter notebook

# Opção 2: Jupyter Lab (mais moderno)
jupyter lab
```

### 5.3 Executar Notebook

1. Navegue até `visualization/fhir_visualization.ipynb`
2. Execute as células em ordem (Shift + Enter)
3. Veja os dados sendo consultados e visualizados

**Você verá:**

- Tabelas com pacientes
- Gráficos de distribuição por gênero
- Lista de observações/exames
- Gráfico de tipos de exames realizados

## 📊 Fluxo Completo Validado

Ao final, você terá validado:

```
✅ 1. Sistema Legado → Dados gerados em formato proprietário
✅ 2. Conector ETL → Transformação Legado → FHIR
✅ 3. Mini HAPI → Armazenamento e API REST FHIR
✅ 4. Visualização → Consulta e exibição dos dados

🎉 BARRAMENTO FHIR FUNCIONANDO PONTA A PONTA!
```

## 🔄 Executar Novamente

Para limpar tudo e recomeçar:

```bash
# Parar serviços e limpar volumes (APAGA DADOS!)
docker-compose down -v

# Reiniciar
docker-compose up -d

# Executar passos 2-5 novamente
```

## 🛠️ Utilitário de Desenvolvimento

Use o menu interativo:

```bash
chmod +x dev-tools.sh
./dev-tools.sh
```

Opções disponíveis:

1. Iniciar ambiente
2. Parar ambiente
3. Rebuild FastAPI
4. Ver logs
5. Acessar banco
6. Executar testes
7. E mais...

## 📝 Checklist de Validação

Marque conforme completa:

- [ ] Docker rodando
- [ ] Mini HAPI respondendo em `/health`
- [ ] Dados legados gerados (2 arquivos JSON)
- [ ] Conector executado com sucesso (100% taxa)
- [ ] Pacientes no banco de dados
- [ ] Observações no banco de dados
- [ ] Swagger UI acessível
- [ ] Jupyter rodando
- [ ] Visualizações exibidas

## ❓ Troubleshooting

### Erro: "Connection refused" no conector

**Solução:** Verifique se o Mini HAPI está rodando:

```bash
docker-compose ps fastapi
docker-compose logs fastapi
```

### Erro: "401 Unauthorized"

**Solução:** Verifique o token em `.env` e no código:

```bash
grep API_TOKEN .env
```

### Erro: "Patient does not exist" ao criar Observation

**Solução:** Execute o conector na ordem correta (pacientes primeiro).

### Nenhum dado no Jupyter

**Solução:** Execute o conector ETL primeiro (Passo 3).

## 📚 Documentação Adicional

- **Mini HAPI**: `fastapi/README.md`
- **Simulador**: `simulator/README.md`
- **Conector**: `connector/README.md`
- **Visualização**: `visualization/README.md`
- **TCC**: `TCC_DOCUMENTATION.md`

## 🎓 Para o TCC

Este fluxo demonstra:

1. **Integração de sistemas legados** com padrões modernos (FHIR)
2. **Processo ETL** completo e funcional
3. **API RESTful** seguindo especificação HL7 FHIR
4. **Persistência de dados** com PostgreSQL
5. **Visualização de dados** científica com Python

---

**Sucesso! Você tem um barramento de saúde FHIR completo e funcional! 🎉**
