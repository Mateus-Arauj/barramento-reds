# 📊 Superset - Visualização de Dados FHIR

## O que é?

Apache Superset é uma plataforma de **Business Intelligence** open-source para criar dashboards interativos e visualizações de dados.

Neste projeto, usamos o Superset para visualizar os dados de pacientes e exames armazenados no barramento FHIR (PostgreSQL).

---

## 🚀 Como Começar?

### Opção 1: Quick Start (5 min)
📄 Veja: **[QUICKSTART.md](QUICKSTART.md)**

### Opção 2: Tutorial Completo
📖 Veja: **[SETUP_SUPERSET.md](SETUP_SUPERSET.md)**

---

## 📋 O que você vai criar?

### Dashboard de Pacientes e Exames

Painéis com visualizações como:

✅ **Métricas:**
- Total de pacientes cadastrados
- Total de exames realizados
- Taxa de pacientes ativos

✅ **Gráficos:**
- Distribuição por gênero (Pizza)
- Pacientes por faixa etária (Barras)
- Top 10 tipos de exames (Barras)
- Status dos exames (Pizza)

✅ **Análises:**
- Exames por paciente
- Evolução temporal
- Dados consolidados

---

## 🎯 Pré-requisitos

1. Superset rodando: `docker compose ps superset`
2. Dados no barramento:
   ```bash
   python3 simulator/legacy_system.py
   python3 connector/fhir_connector.py
   ```

---

## 📊 Acesso

- **URL:** http://localhost:8088
- **Usuário:** admin
- **Senha:** admin123

---

## 📁 Arquivos

- **QUICKSTART.md** - Setup rápido em 5 minutos
- **SETUP_SUPERSET.md** - Tutorial completo passo a passo
- **superset_config.py** - Configuração do Superset

---

## 🔍 Dados Disponíveis

### Tabela: patients
- Nome, gênero, data de nascimento
- Idade calculada
- Status ativo/inativo
- Identificadores (CPF, prontuário)

### Tabela: observations
- Tipo de exame
- Valores e unidades
- Status (final/preliminary)
- Data/hora de realização
- Referência ao paciente

---

## 💡 Dicas

1. Use **SQL Lab** para queries customizadas
2. Campos JSONB: use `->` e `->>`
3. Force refresh com **Ctrl+R** no gráfico
4. Exporte dashboards como PNG/PDF

---

## 📖 Links Úteis

- **Documentação Superset:** https://superset.apache.org
- **SQL PostgreSQL JSONB:** https://www.postgresql.org/docs/current/functions-json.html
- **FHIR R4:** https://hl7.org/fhir/R4/

---

**Projeto MDB-Health - Barramento de Saúde FHIR**
