#!/bin/bash

# Utilitários para desenvolvimento do Mini HAPI

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

show_menu() {
    echo -e "${YELLOW}Mini HAPI - Utilitários de Desenvolvimento${NC}"
    echo "=========================================="
    echo "1. Iniciar ambiente"
    echo "2. Parar ambiente"
    echo "3. Rebuild FastAPI"
    echo "4. Ver logs FastAPI"
    echo "5. Ver logs PostgreSQL"
    echo "6. Acessar banco de dados"
    echo "7. Executar testes"
    echo "8. Executar exemplos Python"
    echo "9. Limpar volumes (⚠️  apaga dados)"
    echo "10. Status dos containers"
    echo "11. Health check"
    echo "0. Sair"
    echo ""
}

start_environment() {
    echo -e "${YELLOW}Iniciando ambiente...${NC}"
    docker-compose up -d --build
    echo -e "${GREEN}✓ Ambiente iniciado${NC}"
    echo "Aguardando serviços ficarem prontos..."
    sleep 5
    docker-compose ps
}

stop_environment() {
    echo -e "${YELLOW}Parando ambiente...${NC}"
    docker-compose down
    echo -e "${GREEN}✓ Ambiente parado${NC}"
}

rebuild_fastapi() {
    echo -e "${YELLOW}Rebuilding FastAPI...${NC}"
    docker-compose up -d --build fastapi
    echo -e "${GREEN}✓ FastAPI rebuilded${NC}"
    sleep 2
    docker-compose logs --tail=50 fastapi
}

view_logs_fastapi() {
    echo -e "${YELLOW}Logs do FastAPI (Ctrl+C para sair):${NC}"
    docker-compose logs -f --tail=100 fastapi
}

view_logs_postgres() {
    echo -e "${YELLOW}Logs do PostgreSQL (Ctrl+C para sair):${NC}"
    docker-compose logs -f --tail=100 postgres
}

access_database() {
    echo -e "${YELLOW}Acessando banco de dados fhir_db...${NC}"
    echo "Comandos úteis:"
    echo "  \dt              - Listar tabelas"
    echo "  \d patients      - Estrutura da tabela patients"
    echo "  \d observations  - Estrutura da tabela observations"
    echo "  SELECT * FROM patients;"
    echo "  \q               - Sair"
    echo ""
    docker exec -it postgres psql -U postgres -d fhir_db
}

run_tests() {
    echo -e "${YELLOW}Executando testes...${NC}"
    cd fastapi
    if [ ! -x test_api.sh ]; then
        chmod +x test_api.sh
    fi
    ./test_api.sh
    cd ..
}

run_examples() {
    echo -e "${YELLOW}Executando exemplos Python...${NC}"
    
    # Verificar se requests está instalado
    if ! python3 -c "import requests" 2>/dev/null; then
        echo -e "${RED}Instalando dependência 'requests'...${NC}"
        pip3 install requests
    fi
    
    cd fastapi
    python3 examples.py
    cd ..
}

clean_volumes() {
    echo -e "${RED}⚠️  ATENÇÃO: Isso irá apagar TODOS os dados!${NC}"
    read -p "Tem certeza? (digite 'sim' para confirmar): " confirm
    
    if [ "$confirm" = "sim" ]; then
        echo -e "${YELLOW}Limpando volumes...${NC}"
        docker-compose down -v
        echo -e "${GREEN}✓ Volumes limpos${NC}"
    else
        echo "Operação cancelada"
    fi
}

check_status() {
    echo -e "${YELLOW}Status dos containers:${NC}"
    docker-compose ps
    echo ""
    echo -e "${YELLOW}Uso de recursos:${NC}"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" $(docker-compose ps -q)
}

health_check() {
    echo -e "${YELLOW}Health check dos serviços...${NC}"
    echo ""
    
    # PostgreSQL
    echo -n "PostgreSQL: "
    if docker exec postgres pg_isready -U postgres > /dev/null 2>&1; then
        echo -e "${GREEN}✓ OK${NC}"
    else
        echo -e "${RED}✗ Falhou${NC}"
    fi
    
    # FastAPI
    echo -n "FastAPI: "
    response=$(curl -s http://localhost:8000/health 2>/dev/null || echo "")
    if echo "$response" | grep -q "ok"; then
        echo -e "${GREEN}✓ OK${NC}"
    else
        echo -e "${RED}✗ Falhou${NC}"
    fi
    
    # HAPI (se estiver rodando)
    if docker-compose ps | grep -q hapi; then
        echo -n "HAPI: "
        hapi_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/fhir/metadata 2>/dev/null || echo "000")
        if [ "$hapi_status" = "200" ]; then
            echo -e "${GREEN}✓ OK${NC}"
        else
            echo -e "${RED}✗ Falhou (HTTP $hapi_status)${NC}"
        fi
    fi
    
    # Superset
    if docker-compose ps | grep -q superset; then
        echo -n "Superset: "
        superset_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8088/health 2>/dev/null || echo "000")
        if [ "$superset_status" = "200" ]; then
            echo -e "${GREEN}✓ OK${NC}"
        else
            echo -e "${RED}✗ Falhou (HTTP $superset_status)${NC}"
        fi
    fi
}

# Menu principal
while true; do
    show_menu
    read -p "Escolha uma opção: " choice
    echo ""
    
    case $choice in
        1) start_environment ;;
        2) stop_environment ;;
        3) rebuild_fastapi ;;
        4) view_logs_fastapi ;;
        5) view_logs_postgres ;;
        6) access_database ;;
        7) run_tests ;;
        8) run_examples ;;
        9) clean_volumes ;;
        10) check_status ;;
        11) health_check ;;
        0) 
            echo -e "${GREEN}Até logo!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Opção inválida${NC}"
            ;;
    esac
    
    echo ""
    read -p "Pressione Enter para continuar..."
    clear
done
