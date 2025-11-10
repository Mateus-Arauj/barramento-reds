#!/bin/bash

# Script de testes para o Mini HAPI
# Uso: ./test_api.sh

set -e

# Configurações
BASE_URL="http://localhost:8000"
TOKEN="${API_TOKEN:-troque-essa-chave}"

echo "🧪 Testando Mini HAPI - Servidor FHIR"
echo "======================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para fazer requisições
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [ -z "$data" ]; then
        curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json"
    else
        curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data"
    fi
}

# Teste 1: Health Check
echo -e "${YELLOW}Teste 1: Health Check${NC}"
response=$(make_request GET "/health")
if echo "$response" | grep -q "ok"; then
    echo -e "${GREEN}✓ Health check passou${NC}"
    echo "$response" | jq .
else
    echo -e "${RED}✗ Health check falhou${NC}"
    exit 1
fi
echo ""

# Teste 2: Metadata
echo -e "${YELLOW}Teste 2: Metadata (CapabilityStatement)${NC}"
response=$(make_request GET "/metadata")
if echo "$response" | grep -q "CapabilityStatement"; then
    echo -e "${GREEN}✓ Metadata retornado${NC}"
    echo "$response" | jq '.resourceType, .software.name'
else
    echo -e "${RED}✗ Metadata falhou${NC}"
    exit 1
fi
echo ""

# Teste 3: Criar Patient
echo -e "${YELLOW}Teste 3: Criar Patient${NC}"
patient_data='{
  "resourceType": "Patient",
  "identifier": [
    {
      "system": "http://hospital.example.org/patients",
      "value": "TEST-'$(date +%s)'"
    }
  ],
  "active": true,
  "name": [
    {
      "use": "official",
      "family": "Silva",
      "given": ["João", "Teste"]
    }
  ],
  "gender": "male",
  "birthDate": "1990-01-15",
  "telecom": [
    {
      "system": "phone",
      "value": "(11) 98765-4321",
      "use": "mobile"
    }
  ]
}'

response=$(make_request POST "/fhir/Patient" "$patient_data")
if echo "$response" | grep -q "Patient"; then
    echo -e "${GREEN}✓ Patient criado${NC}"
    patient_id=$(echo "$response" | jq -r '.id')
    echo "Patient ID: $patient_id"
    echo "$response" | jq '{id, resourceType, name, gender}'
else
    echo -e "${RED}✗ Falha ao criar Patient${NC}"
    echo "$response" | jq .
    exit 1
fi
echo ""

# Teste 4: Buscar Patient
echo -e "${YELLOW}Teste 4: Buscar Patient por ID${NC}"
response=$(make_request GET "/fhir/Patient/$patient_id")
if echo "$response" | grep -q "$patient_id"; then
    echo -e "${GREEN}✓ Patient encontrado${NC}"
    echo "$response" | jq '{id, name, gender, birthDate}'
else
    echo -e "${RED}✗ Falha ao buscar Patient${NC}"
    exit 1
fi
echo ""

# Teste 5: Criar Observation
echo -e "${YELLOW}Teste 5: Criar Observation${NC}"
observation_data='{
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
    "reference": "Patient/'$patient_id'"
  },
  "effectiveDateTime": "2024-01-15T10:30:00Z",
  "valueQuantity": {
    "value": 120,
    "unit": "mmHg",
    "system": "http://unitsofmeasure.org",
    "code": "mm[Hg]"
  }
}'

response=$(make_request POST "/fhir/Observation" "$observation_data")
if echo "$response" | grep -q "Observation"; then
    echo -e "${GREEN}✓ Observation criada${NC}"
    observation_id=$(echo "$response" | jq -r '.id')
    echo "Observation ID: $observation_id"
    echo "$response" | jq '{id, resourceType, status, code, subject}'
else
    echo -e "${RED}✗ Falha ao criar Observation${NC}"
    echo "$response" | jq .
    exit 1
fi
echo ""

# Teste 6: Buscar Observation
echo -e "${YELLOW}Teste 6: Buscar Observation por ID${NC}"
response=$(make_request GET "/fhir/Observation/$observation_id")
if echo "$response" | grep -q "$observation_id"; then
    echo -e "${GREEN}✓ Observation encontrada${NC}"
    echo "$response" | jq '{id, status, subject, valueQuantity}'
else
    echo -e "${RED}✗ Falha ao buscar Observation${NC}"
    exit 1
fi
echo ""

# Teste 7: Buscar Observations do Patient
echo -e "${YELLOW}Teste 7: Buscar Observations do Patient${NC}"
response=$(make_request GET "/fhir/Observation?patient=$patient_id")
if echo "$response" | grep -q "Bundle"; then
    echo -e "${GREEN}✓ Bundle de Observations retornado${NC}"
    total=$(echo "$response" | jq -r '.total')
    echo "Total de observations: $total"
    echo "$response" | jq '{resourceType, type, total}'
else
    echo -e "${RED}✗ Falha ao buscar Observations${NC}"
    exit 1
fi
echo ""

# Teste 8: Buscar Patients
echo -e "${YELLOW}Teste 8: Buscar Patients por nome${NC}"
response=$(make_request GET "/fhir/Patient?name=Silva")
if echo "$response" | grep -q "Bundle"; then
    echo -e "${GREEN}✓ Bundle de Patients retornado${NC}"
    total=$(echo "$response" | jq -r '.total')
    echo "Total de patients encontrados: $total"
else
    echo -e "${RED}✗ Falha ao buscar Patients${NC}"
    exit 1
fi
echo ""

# Teste 9: Atualizar Patient
echo -e "${YELLOW}Teste 9: Atualizar Patient${NC}"
update_data='{
  "resourceType": "Patient",
  "active": false,
  "name": [
    {
      "use": "official",
      "family": "Silva",
      "given": ["João", "Teste", "Atualizado"]
    }
  ],
  "gender": "male",
  "birthDate": "1990-01-15"
}'

response=$(make_request PUT "/fhir/Patient/$patient_id" "$update_data")
if echo "$response" | grep -q "Atualizado"; then
    echo -e "${GREEN}✓ Patient atualizado${NC}"
    version=$(echo "$response" | jq -r '.meta.versionId')
    echo "Nova versão: $version"
else
    echo -e "${RED}✗ Falha ao atualizar Patient${NC}"
    echo "$response" | jq .
    exit 1
fi
echo ""

# Teste 10: Deletar Patient
echo -e "${YELLOW}Teste 10: Deletar Patient${NC}"
status_code=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE_URL/fhir/Patient/$patient_id" \
    -H "Authorization: Bearer $TOKEN")

if [ "$status_code" = "204" ]; then
    echo -e "${GREEN}✓ Patient deletado (HTTP 204)${NC}"
else
    echo -e "${RED}✗ Falha ao deletar Patient (HTTP $status_code)${NC}"
    exit 1
fi
echo ""

# Teste 11: Verificar se Patient foi deletado
echo -e "${YELLOW}Teste 11: Verificar deleção${NC}"
status_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/fhir/Patient/$patient_id" \
    -H "Authorization: Bearer $TOKEN")

if [ "$status_code" = "404" ]; then
    echo -e "${GREEN}✓ Patient não encontrado (HTTP 404) - deleção confirmada${NC}"
else
    echo -e "${RED}✗ Patient ainda existe (HTTP $status_code)${NC}"
    exit 1
fi
echo ""

echo -e "${GREEN}======================================"
echo -e "✓ Todos os testes passaram!"
echo -e "======================================${NC}"
