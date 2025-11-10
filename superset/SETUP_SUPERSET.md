# 📊 Tutorial - Criando Painéis de Pacientes no Superset

## 🎯 Objetivo

Criar dashboards interativos no Apache Superset para visualizar dados de **Pacientes** e **Exames** que já estão armazenados no barramento FHIR (PostgreSQL).

---

## 📋 Antes de Começar

**Certifique-se que você tem:**

- ✅ Superset rodando (`docker compose ps` - deve mostrar superset healthy)
- ✅ Dados no barramento (execute: `python3 simulator/legacy_system.py` e `python3 connector/fhir_connector.py`)

**Verificar se há dados:**

```bash
docker compose exec postgres psql -U pgadmin -d fhir_db -c "SELECT COUNT(*) FROM patients;"
docker compose exec postgres psql -U pgadmin -d fhir_db -c "SELECT COUNT(*) FROM observations;"
```

---

## 🚀 Passo 1: Inicializar o Superset (APENAS NA PRIMEIRA VEZ)

```bash
# Criar admin user
docker compose exec superset superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@example.com \
    --password admin123

# Inicializar o Superset
docker compose exec superset superset db upgrade
docker compose exec superset superset init
```

**Acesse:** http://localhost:8088

- **Usuário:** admin
- **Senha:** admin123

---

## 🔌 Passo 2: Conectar ao Banco de Dados FHIR

### 2.1 Acessar configuração de Database

1. Faça login no Superset (http://localhost:8088)
2. No menu superior direito, clique em **Settings** (⚙️)
3. Selecione **Database Connections**
4. Clique no botão **+ DATABASE**

### 2.2 Configurar conexão PostgreSQL

**Na aba "BASIC":**

```
Display Name: FHIR Database
SQLAlchemy URI: postgresql+psycopg2://pgadmin:pgadmin123@postgres:5432/fhir_db
```

### 2.2 Configurar conexão PostgreSQL

**Selecione:** PostgreSQL

**Preencha:**

- **Display Name:** FHIR Database
- **SQLAlchemy URI:**
  ```
  postgresql+psycopg2://pgadmin:pgadmin123@postgres:5432/fhir_db
  ```

**Clique em:**

1. **TEST CONNECTION** (deve aparecer ✅ "Connection looks good!")
2. **CONNECT**

> 💡 **Explicação da URI:**
>
> - `pgadmin` = usuário do PostgreSQL
> - `pgadmin123` = senha
> - `postgres` = nome do container (hostname)
> - `5432` = porta
> - `fhir_db` = nome do banco de dados

---

## 📊 Passo 3: Adicionar Tabelas (Datasets)

### 3.1 Adicionar tabela de Pacientes

1. Menu superior: **Data** → **Datasets**
2. Clique em **+ DATASET**
3. Preencha:
   - **DATABASE:** FHIR Database
   - **SCHEMA:** public
   - **TABLE:** patients
4. Clique em **ADD**

### 3.2 Adicionar tabela de Observações

Repita o mesmo processo para a tabela **observations**:

1. **+ DATASET**
2. **DATABASE:** FHIR Database
3. **SCHEMA:** public
4. **TABLE:** observations
5. **ADD**

---

## 📈 Passo 4: Criar Seu Primeiro Gráfico

### Gráfico 1: Total de Pacientes

1. Vá em **Data** → **Datasets**
2. Encontre **patients** e clique nele
3. Clique em **CREATE CHART** no canto superior direito
4. Escolha **Big Number** como tipo de visualização
5. Configure:
   - **METRIC:** COUNT(\*)
6. Clique em **CREATE NEW CHART**
7. Clique em **UPDATE CHART** para ver o resultado
8. Clique em **SAVE** e dê um nome: "Total de Pacientes"

### Gráfico 2: Pacientes por Gênero (Pizza)

1. Crie novo chart a partir do dataset **patients**
2. Tipo: **Pie Chart**
3. Configure:
   - **DIMENSIONS:** gender
   - **METRIC:** COUNT(\*)
4. Clique em **UPDATE CHART**
5. Personalize:
   - Aba **CUSTOMIZE**
   - **Chart Title:** "Distribuição por Gênero"
   - **Show Labels:** ✅ Sim
6. **SAVE** como "Pacientes por Gênero"

### Gráfico 3: Total de Exames Realizados

1. Dataset: **observations**
2. Tipo: **Big Number**
3. Configure:
   - **METRIC:** COUNT(\*)
4. **UPDATE CHART**
5. **SAVE** como "Total de Exames"

### Gráfico 4: Tipos de Exames (Barras)

1. Dataset: **observations**
2. Tipo: **Bar Chart**
3. Configure:
   - **DIMENSIONS:** Clique em **SQL** e cole:
     ```sql
     code_json->>'text'
     ```
   - **METRIC:** COUNT(\*)
   - **SORT BY:** COUNT(\*) descending
   - **ROW LIMIT:** 10
4. **UPDATE CHART**
5. Customize:
   - **Chart Title:** "Top 10 Tipos de Exames"
   - **Show Legend:** Não
6. **SAVE**

### Gráfico 5: Status dos Exames (Pizza)

1. Dataset: **observations**
2. Tipo: **Pie Chart**
3. Configure:
   - **DIMENSIONS:** status
   - **METRIC:** COUNT(\*)
4. **UPDATE CHART**
5. **SAVE** como "Status dos Exames"

---

## 🎨 Passo 5: Criar Dashboard

### 5.1 Criar novo Dashboard

1. Menu: **Dashboards**
2. Clique em **+ DASHBOARD**
3. Nome: **"Painel de Pacientes e Exames FHIR"**
4. Clique em **SAVE**

### 5.2 Adicionar gráficos

1. Clique em **EDIT DASHBOARD** (ícone de lápis no canto superior direito)
2. Na barra lateral direita, você verá todos os charts que criou
3. **Arraste e solte** os gráficos no dashboard
4. **Redimensione** cada gráfico arrastando os cantos

**Layout sugerido:**

```
┌─────────────────────────────────────────────────────────────┐
│  Painel de Pacientes e Exames FHIR                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐    ┌──────────────────────────────┐  │
│  │ Total Pacientes  │    │  Total de Exames Realizados  │  │
│  │   (Big Number)   │    │      (Big Number)            │  │
│  └──────────────────┘    └──────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Distribuição por Gênero (Pie Chart)               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Top 10 Tipos de Exames (Bar Chart)                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Status dos Exames (Pie Chart)                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

5. Clique em **SAVE** para salvar o dashboard

---

## 🔍 Passo 6: Queries SQL Avançadas (Opcional)

Para análises mais complexas, use o **SQL Lab**:

1. Menu: **SQL** → **SQL Lab**
2. Selecione: **FHIR Database**
3. Digite sua query

### Exemplo 1: Pacientes com Informações Completas

```sql
SELECT
  id,
  name_json->0->>'text' as nome,
  gender as sexo,
  birth_date as nascimento,
  EXTRACT(YEAR FROM AGE(CAST(birth_date AS DATE))) as idade,
  CASE
    WHEN active = 'true' THEN 'Ativo'
    ELSE 'Inativo'
  END as status
FROM patients
ORDER BY nome
LIMIT 100;
```

### Exemplo 2: Contagem de Exames por Paciente

```sql
SELECT
  p.name_json->0->>'text' as paciente,
  p.gender as sexo,
  COUNT(o.id) as total_exames
FROM patients p
LEFT JOIN observations o ON o.patient_id = p.id
GROUP BY p.id, p.name_json, p.gender
ORDER BY total_exames DESC
LIMIT 20;
```

### Exemplo 3: Exames Detalhados

```sql
SELECT
  p.name_json->0->>'text' as paciente,
  o.code_json->>'text' as exame,
  o.value_quantity_json->>'value' as valor,
  o.value_quantity_json->>'unit' as unidade,
  o.status,
  o.created_at::date as data
FROM observations o
JOIN patients p ON p.id = o.patient_id
ORDER BY o.created_at DESC
LIMIT 50;
```

**Depois de executar:**

- Clique em **EXPLORE** para transformar o resultado em gráfico
- Ou clique em **SAVE DATASET** para criar um dataset virtual

---

## 🎯 Dicas Importantes

### ✅ Boas Práticas

1. **Nomes descritivos:** Use nomes claros para charts e dashboards
2. **Cores consistentes:** Mantenha um padrão de cores no dashboard
3. **Limite de dados:** Use ROW LIMIT em queries grandes
4. **Cache:** O Superset cacheia resultados automaticamente

### 🔄 Atualizar Dados

Quando adicionar novos dados ao barramento:

1. Execute novamente:

   ```bash
   python3 simulator/legacy_system.py
   python3 connector/fhir_connector.py
   ```

2. No Superset, force refresh:
   - Abra o dashboard
   - Clique no ícone **⟳** (refresh) no canto superior direito
   - Ou pressione **Ctrl+R** no gráfico

### 🎨 Personalizar Gráficos

Na aba **CUSTOMIZE** de cada chart você pode:

- Alterar cores
- Adicionar/remover legendas
- Mudar fontes e tamanhos
- Adicionar anotações
- Definir formatação de números

### 📊 Tipos de Gráficos Úteis

| Tipo            | Quando Usar                    |
| --------------- | ------------------------------ |
| **Big Number**  | KPIs, totais, médias           |
| **Pie Chart**   | Distribuições (gênero, status) |
| **Bar Chart**   | Rankings, comparações          |
| **Time Series** | Evolução temporal              |
| **Table**       | Dados detalhados               |
| **Treemap**     | Hierarquias                    |

---

## 🔧 Troubleshooting

### ❌ "Cannot connect to database"

**Solução:**

```bash
# Verificar se postgres está rodando
docker compose ps postgres

# Testar conexão manual
docker compose exec postgres psql -U pgadmin -d fhir_db -c "SELECT 1;"
```

### ❌ "No data to display"

**Solução:**

```bash
# Verificar se há dados
docker compose exec postgres psql -U pgadmin -d fhir_db -c "
  SELECT
    (SELECT COUNT(*) FROM patients) as pacientes,
    (SELECT COUNT(*) FROM observations) as exames;
"
```

Se retornar 0, execute:

```bash
python3 simulator/legacy_system.py
python3 connector/fhir_connector.py
```

### ❌ "Column not found" em gráficos

**Solução:**

1. Vá em **Data** → **Datasets**
2. Clique no dataset problemático
3. Clique em **⋮** (três pontos) → **Edit**
4. Aba **Columns**
5. Clique em **SYNC COLUMNS FROM SOURCE**
6. **SAVE**

### ❌ Gráfico não atualiza após adicionar dados

**Solução:**

1. No gráfico, clique em **⋮** → **Force refresh**
2. Ou limpe o cache:
   - **Settings** → **Database Connections**
   - Selecione **FHIR Database**
   - Clique em **CLEAR CACHE**

---

## 📚 Estrutura dos Dados FHIR

### Tabela: patients

| Coluna        | Tipo      | Descrição                         |
| ------------- | --------- | --------------------------------- |
| id            | string    | ID único do paciente (UUID)       |
| name_json     | jsonb     | Nome completo (estrutura FHIR)    |
| gender        | string    | male/female/other                 |
| birth_date    | string    | Data de nascimento (YYYY-MM-DD)   |
| active        | string    | "true"/"false"                    |
| identifier    | jsonb     | Identificadores (CPF, prontuário) |
| resource_json | jsonb     | Recurso FHIR completo             |
| created_at    | timestamp | Data de cadastro                  |

**Exemplo de acesso aos campos JSON:**

```sql
-- Nome completo
name_json->0->>'text'

-- CPF
identifier->1->>'value'

-- Verificar se está ativo
CASE WHEN active = 'true' THEN 'Sim' ELSE 'Não' END
```

### Tabela: observations

| Coluna              | Tipo      | Descrição                     |
| ------------------- | --------- | ----------------------------- |
| id                  | string    | ID único da observação (UUID) |
| patient_id          | string    | Referência ao paciente        |
| code_json           | jsonb     | Tipo do exame                 |
| value_quantity_json | jsonb     | Valor + unidade               |
| status              | string    | final/preliminary/amended     |
| effective_datetime  | string    | Data/hora do exame            |
| resource_json       | jsonb     | Recurso FHIR completo         |
| created_at          | timestamp | Data de cadastro              |

**Exemplo de acesso aos campos JSON:**

```sql
-- Nome do exame
code_json->>'text'

-- Valor do resultado
(value_quantity_json->>'value')::numeric

-- Unidade de medida
value_quantity_json->>'unit'

-- Juntar com paciente
FROM observations o
JOIN patients p ON o.patient_id = p.id
```

---

## 🎓 Próximos Passos

1. ✅ Explore outros tipos de gráficos na galeria do Superset
2. ✅ Crie dashboards específicos (ex: "Pacientes Pediátricos", "Exames Laboratoriais")
3. ✅ Use filtros interativos (Date Range, Select Filter)
4. ✅ Configure alertas automáticos (se habilitado)
5. ✅ Exporte dashboards como imagem ou PDF

---

## 📖 Recursos

- **Documentação Superset:** https://superset.apache.org/docs/intro
- **SQL do PostgreSQL:** https://www.postgresql.org/docs/current/functions-json.html
- **FHIR R4:** https://hl7.org/fhir/R4/

---

**Criado para o projeto MDB-Health - TCC**
**Sistema de Barramento de Saúde com HL7 FHIR**
