# Simulador de Sistema Legado

Simula um sistema hospitalar legado (como Oracle Soul MV) gerando dados em formato proprietário/não-FHIR.

## Objetivo

Gerar dados de pacientes e exames em um formato customizado que simula a saída de um sistema legado real, antes da transformação para FHIR.

## Uso

```bash
# Executar o simulador
python simulator/legacy_system.py
```

## Saída

O simulador gera dois arquivos JSON:

### `data/patients_legacy.json`

Contém pacientes com campos do sistema legado:

- `PACIENTE_ID` - ID interno do sistema
- `NOME_COMPLETO` - Nome do paciente
- `DATA_NASCIMENTO` - Formato DD/MM/YYYY
- `SEXO` - M/F
- `CPF` - Documento
- `PRONTUARIO` - Número de prontuário
- Endereço, telefones, etc.

### `data/exams_legacy.json`

Contém resultados de exames:

- `EXAME_ID` - ID do exame
- `PACIENTE_ID` - Referência ao paciente
- `CODIGO_EXAME` - Código interno
- `NOME_EXAME` - Nome do exame
- `VALOR_RESULTADO` - Valor numérico
- `UNIDADE_MEDIDA` - Unidade (mg/dL, mmHg, etc.)
- `STATUS_RESULTADO` - NORMAL/ALTERADO/CRITICO
- Datas, médico solicitante, etc.

## Exemplo de Dados

### Paciente

```json
{
  "PACIENTE_ID": "PAC123456",
  "NOME_COMPLETO": "João Silva Santos",
  "DATA_NASCIMENTO": "15/05/1980",
  "SEXO": "M",
  "CPF": "123.456.789-00",
  "PRONTUARIO": "PRONT-12345",
  "TELEFONE_1": "(11) 98765-4321",
  "EMAIL": "joao.santos@email.com",
  "ENDERECO_RUA": "Rua das Flores, 123",
  "ENDERECO_CIDADE": "São Paulo",
  "ENDERECO_ESTADO": "SP",
  "STATUS_ATIVO": "S"
}
```

### Exame

```json
{
  "EXAME_ID": "EXM789012",
  "PACIENTE_ID": "PAC123456",
  "CODIGO_EXAME": "GLI001",
  "NOME_EXAME": "Glicemia em Jejum",
  "VALOR_RESULTADO": 95.5,
  "UNIDADE_MEDIDA": "mg/dL",
  "VALOR_REFERENCIA_MIN": 70,
  "VALOR_REFERENCIA_MAX": 99,
  "STATUS_RESULTADO": "NORMAL",
  "DATA_COLETA": "15/01/2024 08:30"
}
```

## Configuração

Edite `legacy_system.py` para ajustar:

- Número de pacientes gerados
- Número de exames por paciente
- Tipos de exames disponíveis
- Cidades e outros dados demográficos
