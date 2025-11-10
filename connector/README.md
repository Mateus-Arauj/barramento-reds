# Conector ETL - Sistema Legado → FHIR

Transforma dados do sistema legado em recursos FHIR e os envia para o Mini HAPI.

## Objetivo

Implementar o processo ETL (Extract, Transform, Load):

1. **Extract**: Lê dados do sistema legado (simulador)
2. **Transform**: Converte dados proprietários para recursos FHIR válidos
3. **Load**: Envia recursos FHIR para o servidor Mini HAPI

## Pré-requisitos

1. Servidor Mini HAPI rodando (`docker-compose up -d`)
2. Dados legados gerados (`python simulator/legacy_system.py`)

## Uso

```bash
# Executar o conector
python connector/fhir_connector.py
```

## Transformações Implementadas

### Patient (Paciente)

| Campo Legado                   | Campo FHIR         | Transformação         |
| ------------------------------ | ------------------ | --------------------- |
| `PACIENTE_ID`                  | `identifier.value` | Direto                |
| `NOME_COMPLETO`                | `name`             | Split em given/family |
| `SEXO` (M/F)                   | `gender`           | M→male, F→female      |
| `DATA_NASCIMENTO` (DD/MM/YYYY) | `birthDate`        | DD/MM/YYYY→YYYY-MM-DD |
| `CPF`                          | `identifier`       | Sistema CPF           |
| `STATUS_ATIVO` (S/N)           | `active`           | S→true, N→false       |
| `TELEFONE_1`                   | `telecom`          | ContactPoint          |
| `ENDERECO_RUA`                 | `address.line`     | Address               |

### Observation (Observação/Exame)

| Campo Legado                     | Campo FHIR                  | Transformação   |
| -------------------------------- | --------------------------- | --------------- |
| `EXAME_ID`                       | `identifier.value`          | Direto          |
| `CODIGO_EXAME`                   | `code.coding.code`          | CodeableConcept |
| `NOME_EXAME`                     | `code.text`                 | Direto          |
| `VALOR_RESULTADO`                | `valueQuantity.value`       | Direto          |
| `UNIDADE_MEDIDA`                 | `valueQuantity.unit`        | Direto          |
| `STATUS_RESULTADO`               | `status` + `interpretation` | NORMAL→final+N  |
| `DATA_COLETA` (DD/MM/YYYY HH:MM) | `effectiveDateTime`         | ISO 8601        |
| `PACIENTE_ID`                    | `subject.reference`         | Patient/{id}    |

## Exemplo de Transformação

### Entrada (Legado)

```json
{
  "PACIENTE_ID": "PAC123456",
  "NOME_COMPLETO": "João Silva Santos",
  "SEXO": "M",
  "DATA_NASCIMENTO": "15/05/1980"
}
```

### Saída (FHIR)

```json
{
  "resourceType": "Patient",
  "identifier": [
    {
      "system": "http://hospital.example.org/legacy-patient-id",
      "value": "PAC123456"
    }
  ],
  "name": [
    {
      "family": "Santos",
      "given": ["João", "Silva"]
    }
  ],
  "gender": "male",
  "birthDate": "1980-05-15"
}
```

## Estatísticas

O conector exibe estatísticas ao final:

- Total de pacientes processados
- Sucessos e falhas
- Total de observações processadas
- Taxa de sucesso

## Configuração

Variáveis de ambiente:

```bash
export FHIR_BASE_URL="http://localhost:8000"
export API_TOKEN="seu-token"
```

## Logs

O conector exibe logs detalhados:

```
📋 Processando paciente: João Silva Santos (PAC123456)
  🔄 Transformando para FHIR Patient...
  📤 Enviando Patient para Mini HAPI...
  ✓ Patient criado com ID: uuid-gerado
  🔄 Processando 5 exames...
    ✓ Observation Glicemia em Jejum: obs-id-1
    ✓ Observation Hemograma Completo: obs-id-2
```
