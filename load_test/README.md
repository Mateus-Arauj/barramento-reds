# 🔥 Teste de Carga - Mini HAPI FHIR Server

Este diretório contém testes de carga usando **Locust** para avaliar a performance do servidor FHIR.

## 📦 Instalação

```bash
cd load_test
pip install -r requirements.txt
```

## 🚀 Como Executar

### Modo 1: Interface Web (Recomendado)

```bash
locust -f locustfile.py --host=http://localhost:8000
```

Depois acesse: **http://localhost:8089**

Na interface web:

- **Number of users**: 10 (usuários simultâneos)
- **Spawn rate**: 2 (usuários/segundo)
- Clique em **Start swarming**

### Modo 2: Linha de Comando (Headless)

Teste rápido com 10 usuários por 60 segundos:

```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 10 \
  --spawn-rate 2 \
  --run-time 60s \
  --headless \
  --html report.html
```

Teste intenso com 100 usuários:

```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 100 \
  --spawn-rate 10 \
  --run-time 300s \
  --headless \
  --html report_100users.html
```

## 📊 O que é Testado

O teste simula usuários reais realizando operações no servidor FHIR:

| Operação             | Peso | Descrição                                |
| -------------------- | ---- | ---------------------------------------- |
| `create_patient`     | 3x   | Cria novos pacientes com dados fictícios |
| `get_patient`        | 2x   | Busca pacientes existentes por ID        |
| `create_observation` | 2x   | Cria observações/exames para pacientes   |
| `get_observation`    | 1x   | Busca observações existentes             |
| `search_patients`    | 1x   | Busca pacientes com filtros              |
| `health_check`       | 1x   | Verifica saúde do sistema                |

**Peso**: Define a frequência relativa de cada operação. 3x significa que é executado 3 vezes mais que operações com peso 1x.

## 📈 Métricas Importantes

Ao executar o teste, observe:

- **Requests/s (RPS)**: Quantas requisições por segundo o sistema aguenta
- **Response time**: Tempo médio de resposta (ideal < 500ms)
- **Failures**: Taxa de falhas (ideal 0%)
- **95th percentile**: 95% das requisições responderam em X ms

### Benchmarks Esperados

Para um servidor FastAPI + PostgreSQL rodando localmente:

| Usuários | RPS Esperado | Response Time (p95) |
| -------- | ------------ | ------------------- |
| 10       | 50-100       | < 200ms             |
| 50       | 200-400      | < 500ms             |
| 100      | 300-600      | < 1s                |

## 🔧 Configuração

### Ajustar Token de Autenticação

Se seu servidor usa autenticação, edite o token em `locustfile.py`:

```python
self.headers = {
    "Content-Type": "application/fhir+json",
    "Authorization": "Bearer SEU-TOKEN-AQUI"
}
```

### Ajustar Host

Se o servidor não estiver em `localhost:8000`:

```bash
locust -f locustfile.py --host=http://seu-servidor:porta
```

## 📝 Exemplos de Uso

### Encontrar o Limite do Sistema

Execute testes progressivos até encontrar o ponto de quebra:

```bash
# 10 usuários
locust -f locustfile.py --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 60s --headless

# 50 usuários
locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 60s --headless

# 100 usuários
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 60s --headless

# 200 usuários
locust -f locustfile.py --host=http://localhost:8000 --users 200 --spawn-rate 20 --run-time 60s --headless
```

### Teste de Estresse (Spike Test)

Simula um pico súbito de tráfego:

```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 500 \
  --spawn-rate 50 \
  --run-time 30s \
  --headless
```

### Teste de Resistência (Soak Test)

Executa por tempo prolongado para detectar memory leaks:

```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 20 \
  --spawn-rate 2 \
  --run-time 30m \
  --headless \
  --html soak_test.html
```

## 📊 Interpretando Resultados

### Interface Web

A interface mostra gráficos em tempo real:

- **Total Requests per Second**: Throughput do sistema
- **Response Times**: Latência (50th, 95th, 99th percentile)
- **Number of Users**: Quantos usuários simulados estão ativos

### Relatório HTML

O relatório HTML (`--html report.html`) contém:

- Estatísticas detalhadas por endpoint
- Gráficos de evolução temporal
- Taxa de falhas
- Distribuição de tempos de resposta

### Exemplo de Saída (Console)

```
Name                                          # reqs      # fails  |     Avg     Min     Max  Median  |   req/s failures/s
--------------------------------------------------------------------------------------------------------
POST /fhir/Patient                              1234           0  |     120      45     890     110  |   20.5     0.00
GET /fhir/Patient/{id}                           823           0  |      85      35     456      80  |   13.7     0.00
POST /fhir/Observation                           789           2  |     145      52    1200     130  |   13.2     0.03
GET /fhir/Observation/{id}                       456           0  |      92      38     567      85  |    7.6     0.00
GET /fhir/Patient?filters                        401           0  |     156      65     789     145  |    6.7     0.00
GET /health                                      398           0  |      12       5      89      10  |    6.6     0.00
--------------------------------------------------------------------------------------------------------
Aggregated                                      4101           2  |     110      5     1200     100  |   68.3     0.03
```

## 🐛 Troubleshooting

### Muitas Falhas (High Failure Rate)

1. Verifique se o servidor está rodando: `curl http://localhost:8000/health`
2. Confira o token de autenticação no código
3. Verifique logs do servidor: `docker-compose logs -f fastapi`

### Response Time Alto

1. Verifique recursos do sistema: `htop` ou `docker stats`
2. Aumente recursos do container (memória, CPU)
3. Otimize queries do banco de dados
4. Adicione índices no PostgreSQL

### Erros de Conexão

1. Verifique se o host está correto
2. Desative firewall local temporariamente
3. Aumente o timeout do Locust:

```python
class FHIRUser(HttpUser):
    network_timeout = 10.0  # segundos
```

## 💡 Dicas

1. **Warm-up**: Sempre faça alguns testes leves antes do teste principal
2. **Monitoramento**: Use `docker stats` ou `htop` para ver uso de recursos
3. **Banco de dados**: Monitore conexões PostgreSQL durante o teste
4. **Limpeza**: Limpe o banco após testes: `docker-compose down -v && docker-compose up -d`

## 📚 Documentação

- [Locust Documentation](https://docs.locust.io/)
- [Writing a Locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html)
- [Performance Testing Best Practices](https://docs.locust.io/en/stable/running-locust-distributed.html)

## 🎯 Próximos Passos

Após executar os testes:

1. Identifique endpoints mais lentos
2. Otimize queries do banco
3. Adicione cache se necessário
4. Configure connection pooling
5. Considere adicionar rate limiting
