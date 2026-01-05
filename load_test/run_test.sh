#!/bin/bash

# Script para executar testes de carga de forma fácil

set -e

echo "🔥 Mini HAPI FHIR - Teste de Carga"
echo "=================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verifica se locust está instalado
if ! command -v locust &> /dev/null; then
    echo -e "${RED}❌ Locust não encontrado!${NC}"
    echo "Instalando..."
    pip install -r requirements.txt
fi

# Verifica se o servidor está rodando
echo -e "${YELLOW}Verificando servidor...${NC}"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Servidor está rodando${NC}"
else
    echo -e "${RED}❌ Servidor não está rodando!${NC}"
    echo "Execute: docker-compose up -d"
    exit 1
fi

echo ""
echo "Escolha o tipo de teste:"
echo "1) Interface Web (Recomendado para iniciantes)"
echo "2) Teste Rápido - 10 usuários, 60s"
echo "3) Teste Médio - 50 usuários, 120s"
echo "4) Teste Intenso - 100 usuários, 180s"
echo "5) Teste de Estresse - 200 usuários, 60s"
echo "6) Personalizado"
read -p "Opção [1-6]: " option

case $option in
    1)
        echo -e "${GREEN}Iniciando interface web...${NC}"
        echo "Acesse: http://localhost:8089"
        locust -f locustfile.py --host=http://localhost:8000
        ;;
    2)
        echo -e "${GREEN}Executando teste rápido...${NC}"
        locust -f locustfile.py \
            --host=http://localhost:8000 \
            --users 10 \
            --spawn-rate 2 \
            --run-time 60s \
            --headless \
            --html reports/quick_test_$(date +%Y%m%d_%H%M%S).html
        ;;
    3)
        echo -e "${GREEN}Executando teste médio...${NC}"
        locust -f locustfile.py \
            --host=http://localhost:8000 \
            --users 50 \
            --spawn-rate 5 \
            --run-time 120s \
            --headless \
            --html reports/medium_test_$(date +%Y%m%d_%H%M%S).html
        ;;
    4)
        echo -e "${GREEN}Executando teste intenso...${NC}"
        locust -f locustfile.py \
            --host=http://localhost:8000 \
            --users 100 \
            --spawn-rate 10 \
            --run-time 180s \
            --headless \
            --html reports/intense_test_$(date +%Y%m%d_%H%M%S).html
        ;;
    5)
        echo -e "${YELLOW}⚠️  Teste de Estresse - Pode causar lentidão!${NC}"
        read -p "Continuar? (s/n): " confirm
        if [ "$confirm" = "s" ]; then
            echo -e "${GREEN}Executando teste de estresse...${NC}"
            locust -f locustfile.py \
                --host=http://localhost:8000 \
                --users 200 \
                --spawn-rate 20 \
                --run-time 60s \
                --headless \
                --html reports/stress_test_$(date +%Y%m%d_%H%M%S).html
        fi
        ;;
    6)
        read -p "Número de usuários: " users
        read -p "Taxa de spawn (usuários/s): " spawn_rate
        read -p "Duração (segundos): " duration
        echo -e "${GREEN}Executando teste personalizado...${NC}"
        locust -f locustfile.py \
            --host=http://localhost:8000 \
            --users $users \
            --spawn-rate $spawn_rate \
            --run-time ${duration}s \
            --headless \
            --html reports/custom_test_$(date +%Y%m%d_%H%M%S).html
        ;;
    *)
        echo -e "${RED}Opção inválida!${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✓ Teste concluído!${NC}"
echo "Relatórios salvos em: load_test/reports/"
