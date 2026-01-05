# 🐳 Teste de Carga - Executando no Container

Script Python simples que **roda dentro do container** sem precisar instalar Locust.

## 🚀 Como Executar

### Opção 1: Script Automatizado (Recomendado)

```bash
# Teste padrão: 10 usuários por 60 segundos
./load_test/run_test_docker.sh

# Teste personalizado
./load_test/run_test_docker.sh --users 50 --duration 120

# Teste intenso
./load_test/run_test_docker.sh --users 100 --duration 180
```

### Opção 2: Manualmente no Container

```bash
# Copia o script para o container
docker cp load_test/load_test_simple.py fastapi:/tmp/load_test_simple.py

# Executa dentro do container
docker exec -it fastapi python3 /tmp/load_test_simple.py \
  --url http://localhost:8000 \
  --token test-token \
  --users 10 \
  --duration 60
```

### Opção 3: Direto da sua máquina (se tiver Python)

```bash
cd load_test
pip install requests  # se não tiver
python3 load_test_simple.py --users 10 --duration 60
```

## 📊 Parâmetros

| Parâmetro    | Padrão                  | Descrição                      |
| ------------ | ----------------------- | ------------------------------ |
| `--url`      | `http://localhost:8000` | URL do servidor FHIR           |
| `--token`    | `test-token`            | Token de autenticação          |
| `--users`    | `10`                    | Número de usuários simultâneos |
| `--duration` | `60`                    | Duração do teste em segundos   |

## 📈 Exemplo de Saída

```
============================================================
🔥 Teste de Carga - Mini HAPI FHIR Server
============================================================
URL: http://localhost:8000
Usuários simultâneos: 10
Duração: 60s
============================================================

Verificando servidor...
✓ Servidor está respondendo

Iniciando teste...

👤 Usuário 1 iniciado
👤 Usuário 2 iniciado
...

============================================================
📊 RESULTADOS DO TESTE
============================================================

Duração total: 60.12s
Total de requisições: 487
Requisições bem-sucedidas: 485 (99.6%)
Requisições falhas: 2 (0.4%)
Requisições/segundo (RPS): 8.10

Estatísticas por Endpoint:
------------------------------------------------------------
Endpoint                                 Reqs     Falhas   Avg(ms)    p95(ms)
------------------------------------------------------------
POST /fhir/Patient                       156      0        145.23     289.45
GET /fhir/Patient/{id}                   104      0        78.56      156.32
POST /fhir/Observation                   98       1        167.89     312.67
GET /fhir/Observation/{id}               52       0        82.34      178.90
GET /fhir/Patient?filters                45       0        124.56     245.78
GET /health                              32       1        12.34      23.45
------------------------------------------------------------

Tempos de Resposta (ms):
  Mínimo: 8.23ms
  Médio: 112.45ms
  Mediana: 98.67ms
  Máximo: 456.78ms
  P95: 278.90ms
  P99: 389.12ms

✓ Teste concluído!
============================================================
```

## 🎯 Interpretação dos Resultados

### Métricas Importantes:

- **RPS (Requests/s)**: Quantas requisições o sistema aguenta por segundo

  - 5-10 RPS: Baixo (adequado para sistemas internos)
  - 10-50 RPS: Médio (bom para aplicações pequenas/médias)
  - 50-100+ RPS: Alto (excelente performance)

- **Taxa de Sucesso**: Deve ser > 99%

  - < 95%: Sistema instável
  - 95-99%: Aceitável mas precisa investigar
  - > 99%: Excelente

- **Tempo de Resposta (p95)**: 95% das requisições devem responder em:
  - < 200ms: Excelente
  - 200-500ms: Bom
  - 500ms-1s: Aceitável
  - > 1s: Precisa otimização

## 🔧 Testes Progressivos

Execute testes com carga crescente para encontrar o limite:

```bash
# Teste leve
./load_test/run_test_docker.sh --users 5 --duration 30

# Teste médio
./load_test/run_test_docker.sh --users 10 --duration 60

# Teste pesado
./load_test/run_test_docker.sh --users 25 --duration 60

# Teste intenso
./load_test/run_test_docker.sh --users 50 --duration 60

# Teste de estresse
./load_test/run_test_docker.sh --users 100 --duration 60
```

Observe quando a taxa de falhas aumenta ou o tempo de resposta dispara.

## 🐛 Troubleshooting

### Erro: Container não está rodando

```bash
docker-compose up -d
```

### Muitas falhas (> 5%)

1. Verifique logs: `docker-compose logs -f fastapi`
2. Verifique recursos: `docker stats`
3. Reduza número de usuários

### "Connection refused"

1. Certifique-se que o servidor está rodando
2. Verifique a URL (deve ser `http://localhost:8000`)
3. Execute dentro do container para evitar problemas de rede

## 💡 Vantagens deste Método

✅ **Sem instalação extra**: Usa apenas Python + requests  
✅ **Roda no container**: Não precisa configurar ambiente local  
✅ **Leve**: Não precisa do Locust ou outras ferramentas pesadas  
✅ **Simples**: Código Python puro, fácil de entender e modificar  
✅ **Portável**: Funciona em qualquer lugar que tenha Python

## 🆚 Comparação: Simple vs Locust

| Característica | load_test_simple.py | Locust               |
| -------------- | ------------------- | -------------------- |
| Instalação     | Apenas `requests`   | Precisa `locust`     |
| Interface      | Terminal/CLI        | Web UI bonita        |
| Relatórios     | Console             | HTML + gráficos      |
| Complexidade   | Simples             | Médio/Avançado       |
| Performance    | ~100 usuários       | 1000+ usuários       |
| Uso            | Testes rápidos      | Testes profissionais |

**Recomendação**:

- Use `load_test_simple.py` para testes rápidos e desenvolvimento
- Use `Locust` (locustfile.py) para testes profissionais e apresentações
