# Visualização de Dados FHIR

Jupyter Notebook para consultar e visualizar dados do Mini HAPI.

## Objetivo

Demonstrar o barramento funcionando ponta a ponta através de visualizações e análises dos dados FHIR.

## Pré-requisitos

1. Servidor Mini HAPI rodando
2. Dados carregados via conector ETL
3. Dependências Python instaladas

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
# Iniciar Jupyter
jupyter notebook

# Ou Jupyter Lab
jupyter lab
```

Abra o notebook: `visualization/fhir_visualization.ipynb`

## Conteúdo do Notebook

### 1. Configuração

- Importação de bibliotecas
- Configuração da conexão com Mini HAPI
- Funções auxiliares

### 2. Consulta de Pacientes

- Busca todos os pacientes via API
- Exibe em formato tabular (pandas DataFrame)
- Estatísticas básicas

### 3. Visualizações de Pacientes

- Distribuição por gênero (gráfico de pizza)
- Status ativo/inativo (gráfico de barras)

### 4. Consulta de Observações

- Busca observações de paciente específico
- Exibe resultados de exames
- Relaciona paciente ↔ observações

### 5. Análise Agregada

- Distribuição de tipos de exames
- Gráfico de barras horizontal
- Estatísticas gerais

### 6. Demonstração Ponta a Ponta

- Confirma que todo o fluxo está funcionando
- Valida transformações
- Próximos passos

## Bibliotecas Utilizadas

- **requests**: Chamadas HTTP para API FHIR
- **pandas**: Manipulação e análise de dados
- **matplotlib**: Visualizações básicas
- **seaborn**: Visualizações estilizadas

## Exemplos de Saída

### Tabela de Pacientes

```
| ID         | Nome            | Gênero | Data Nascimento | Ativo |
|------------|-----------------|--------|-----------------|-------|
| abc-123    | João Silva      | male   | 1980-05-15      | True  |
| def-456    | Maria Santos    | female | 1992-03-20      | True  |
```

### Gráficos

- Pizza: Distribuição de gêneros
- Barras: Tipos de exames realizados
- Barras: Status dos pacientes

## Configuração

Variáveis de ambiente (opcionais):

```bash
export FHIR_BASE_URL="http://localhost:8000"
export API_TOKEN="seu-token"
```

Ou edite diretamente no notebook.

## Próximas Melhorias

- [ ] Filtros interativos
- [ ] Gráficos de séries temporais
- [ ] Dashboards com Plotly Dash
- [ ] Integração com Superset
- [ ] Exportação de relatórios PDF
