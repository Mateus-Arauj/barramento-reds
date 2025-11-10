#!/bin/bash
# Script de teste completo do sistema MDB-Health

set -e  # Para em caso de erro

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          TESTE COMPLETO DO SISTEMA MDB-HEALTH                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configurações
API_URL="http://localhost:8000"
TOKEN="troque-essa-chave"  # Deve ser o mesmo do .env

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  PASSO 1: Verificar containers${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
docker compose ps
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  PASSO 2: Verificar saúde da API${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
curl -s $API_URL/health | python3 -m json.tool
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  PASSO 3: Gerar dados legados (Simulador)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
python3 simulator/legacy_system.py
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  PASSO 4: Executar ETL (Conector)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
python3 connector/fhir_connector.py
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  PASSO 5: Testar API - Criar Patient${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
PATIENT_RESPONSE=$(curl -s -X POST $API_URL/fhir/Patient \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/fhir+json" \
  -d '{
    "resourceType": "Patient",
    "name": [{
      "family": "Teste",
      "given": ["Paciente", "Exemplo"]
    }],
    "gender": "male",
    "birthDate": "1985-03-20"
  }')

echo "$PATIENT_RESPONSE" | python3 -m json.tool
PATIENT_ID=$(echo "$PATIENT_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo ""
echo -e "${GREEN}✓ Patient criado com ID: $PATIENT_ID${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  PASSO 6: Testar API - Buscar Patient${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
curl -s $API_URL/fhir/Patient/$PATIENT_ID \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  PASSO 7: Testar API - Criar Observation${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
OBSERVATION_RESPONSE=$(curl -s -X POST $API_URL/fhir/Observation \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/fhir+json" \
  -d "{
    \"resourceType\": \"Observation\",
    \"status\": \"final\",
    \"code\": {
      \"coding\": [{
        \"system\": \"http://loinc.org\",
        \"code\": \"85354-9\",
        \"display\": \"Blood pressure\"
      }],
      \"text\": \"Pressão Arterial\"
    },
    \"subject\": {
      \"reference\": \"Patient/$PATIENT_ID\"
    },
    \"effectiveDateTime\": \"2024-01-15T10:30:00Z\",
    \"valueQuantity\": {
      \"value\": 120,
      \"unit\": \"mmHg\",
      \"system\": \"http://unitsofmeasure.org\",
      \"code\": \"mm[Hg]\"
    }
  }")

echo "$OBSERVATION_RESPONSE" | python3 -m json.tool
OBSERVATION_ID=$(echo "$OBSERVATION_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo ""
echo -e "${GREEN}✓ Observation criada com ID: $OBSERVATION_ID${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  PASSO 8: Verificar banco de dados${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "Contando recursos no banco..."
docker compose exec -T postgres psql -U pgadmin -d fhir_db -c "SELECT 'Patients' as tipo, COUNT(*) as total FROM patients UNION ALL SELECT 'Observations', COUNT(*) FROM observations;"
echo ""

echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ✓ TESTE COMPLETO FINALIZADO!                  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo "  1. Acesse http://localhost:8000/docs para ver a documentação Swagger"
echo "  2. Acesse http://localhost:8088 para o Superset (admin/admin123)"
echo "  3. Use o Jupyter Notebook em visualization/fhir_visualization.ipynb"
echo ""
