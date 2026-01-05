#!/bin/bash

# Script para rodar teste de carga dentro do container Python
# Usa o container FastAPI existente para executar o teste

set -e

echo "🔥 Executando Teste de Carga no Container"
echo "=========================================="
echo ""

# Verifica se o container está rodando
if ! docker ps | grep -q "fastapi"; then
    echo "❌ Container FastAPI não está rodando!"
    echo "Execute: docker-compose up -d"
    exit 1
fi

# Configurações padrão
URL="http://localhost:8000"
TOKEN="troque-essa-chave"
USERS=10
DURATION=60

# Parse argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --users)
            USERS="$2"
            shift 2
            ;;
        --duration)
            DURATION="$2"
            shift 2
            ;;
        --token)
            TOKEN="$2"
            shift 2
            ;;
        *)
            echo "Opção desconhecida: $1"
            echo "Uso: $0 [--users NUM] [--duration SECONDS] [--token TOKEN]"
            exit 1
            ;;
    esac
done

echo "Configurações do Teste:"
echo "  Usuários: $USERS"
echo "  Duração: ${DURATION}s"
echo "  URL: $URL"
echo ""

# Copia o script para dentro do container
echo "Copiando script para o container..."
docker cp load_test/load_test_simple.py fastapi:/tmp/load_test_simple.py

# Instala requests se necessário e executa o teste
echo "Executando teste..."
echo ""

docker exec -it fastapi python3 /tmp/load_test_simple.py \
    --url "$URL" \
    --token "$TOKEN" \
    --users "$USERS" \
    --duration "$DURATION"

# Limpa o arquivo temporário
docker exec fastapi rm -f /tmp/load_test_simple.py

echo ""
echo "✓ Teste concluído!"
