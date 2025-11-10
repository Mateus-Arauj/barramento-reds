# 🚀 Guia Rápido - Mini HAPI

## Configuração Inicial

### 1. Configurar variáveis de ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env e ajustar as seguintes variáveis:
# - API_TOKEN: Token de autenticação (use um valor seguro)
# - POSTGRES_PASSWORD: Senha do PostgreSQL
# - FHIR_DB_PASS: Senha do banco FHIR
```

### 2. Iniciar o ambiente

```bash
# Build e start de todos os serviços
docker-compose up -d --build

# Verificar logs
docker-compose logs -f fastapi
```

### 3. Testar a API

```bash
# Health check
curl http://localhost:8000/health

# Com jq para formatar
curl http://localhost:8000/metadata | jq .
```

## 📝 Uso Básico

### Criar um Patient

```bash
export TOKEN="seu-token-aqui"

curl -X POST http://localhost:8000/fhir/Patient \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "Patient",
    "name": [{"family": "Silva", "given": ["João"]}],
    "gender": "male",
    "birthDate": "1980-05-15"
  }' | jq .
```

### Buscar Patient

```bash
# Substitua PATIENT_ID pelo ID retornado acima
curl http://localhost:8000/fhir/Patient/PATIENT_ID \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### Criar Observation

```bash
curl -X POST http://localhost:8000/fhir/Observation \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "Observation",
    "status": "final",
    "code": {
      "coding": [{
        "system": "http://loinc.org",
        "code": "85354-9",
        "display": "Blood pressure"
      }],
      "text": "Pressão Arterial"
    },
    "subject": {"reference": "Patient/PATIENT_ID"},
    "effectiveDateTime": "2024-01-15T10:30:00Z",
    "valueQuantity": {"value": 120, "unit": "mmHg"}
  }' | jq .
```

## 🧪 Executar Testes

```bash
# Tornar o script executável
chmod +x fastapi/test_api.sh

# Executar todos os testes
cd fastapi
./test_api.sh
```

## 🐍 Usar o Cliente Python

```bash
# Instalar dependências
pip install requests

# Executar exemplos
cd fastapi
python examples.py
```

## 🗄️ Acessar o Banco de Dados

```bash
# Conectar ao PostgreSQL
docker exec -it postgres psql -U postgres -d fhir_db

# Consultas úteis
SELECT id, name, gender FROM patients;
SELECT id, status, subject_reference FROM observations;
```

## 🔧 Comandos Úteis

```bash
# Parar todos os serviços
docker-compose down

# Reiniciar apenas o FastAPI
docker-compose restart fastapi

# Ver logs em tempo real
docker-compose logs -f fastapi

# Limpar volumes (CUIDADO: apaga dados!)
docker-compose down -v

# Rebuild após mudanças no código
docker-compose up -d --build fastapi
```

## 📊 Estrutura de Resposta

### Patient

```json
{
  "resourceType": "Patient",
  "id": "uuid-gerado",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2024-01-15T10:30:00Z"
  },
  "name": [...],
  "gender": "male",
  "birthDate": "1980-05-15"
}
```

### Observation

```json
{
  "resourceType": "Observation",
  "id": "uuid-gerado",
  "status": "final",
  "code": {...},
  "subject": {"reference": "Patient/..."},
  "valueQuantity": {...}
}
```

### Bundle (para buscas)

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 5,
  "entry": [
    {
      "fullUrl": "/fhir/Patient/...",
      "resource": {...}
    }
  ]
}
```

## ⚠️ Troubleshooting

### Erro de conexão com o banco

```bash
# Verificar se o PostgreSQL está rodando
docker-compose ps postgres

# Ver logs do PostgreSQL
docker-compose logs postgres

# Verificar se o banco foi criado
docker exec -it postgres psql -U postgres -c "\l"
```

### Erro 401 (Unauthorized)

- Verifique se o header Authorization está correto
- Confirme que o token no .env corresponde ao usado na requisição

### Erro 409 (Conflict)

- O recurso com esse ID já existe
- Remova o campo "id" do JSON para gerar um novo UUID automaticamente

### Erro 400 ao criar Observation

- Verifique se o Patient referenciado existe
- Confirme que o campo "status" está presente
- Valide que o campo "code" está correto

## 📚 Recursos Adicionais

- [README completo](./fastapi/README.md)
- [Especificação FHIR R4](https://hl7.org/fhir/R4/)
- [Documentação FastAPI](https://fastapi.tiangolo.com/)

## 🎯 Próximos Passos

1. Testar todos os endpoints
2. Adicionar mais Patients e Observations
3. Explorar os parâmetros de busca
4. Integrar com Superset para visualizações
5. (Opcional) Adicionar novos recursos FHIR

---

**Dica**: Acesse http://localhost:8000/docs para ver a documentação interativa (Swagger UI) da API!
