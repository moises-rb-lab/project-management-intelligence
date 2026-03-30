# ⚡ Project Analytics — Data Intelligence Platform

> **Business Case Data-Driven** — Inteligência aplicada à gestão de projetos  
> Unindo Analytics · Engenharia de Dados · Arquitetura Medalhão

---

## 🎯 Objetivo

Transformar dados brutos de projetos em decisões estratégicas que aumentem a previsibilidade, reduzam atrasos e otimizem custos — através de uma plataforma completa de dados com pipeline ETL, API e visualização desacoplada.

---

## 🔍 Cenário de Ataque (O Problema Real)

A gestão de projetos frequentemente enfrenta desafios críticos que impactam diretamente a eficiência operacional e os resultados do negócio:

| Problema | Impacto |
|----------|---------|
| Baixa previsibilidade de prazos | Dificuldade em cumprir deadlines |
| Estouro de custos | Redução de margem e ROI |
| Falta de visibilidade | Decisões reativas ao invés de estratégicas |
| Performance desigual entre gestores | Ineficiência operacional |

---

## 🏗️ Arquitetura

```
[Ingestão de Dados]
CSV Upload ───────────────► Supabase (PostgreSQL)
│
┌───────────┴───────────┐
▼ ▼
🥉 Bronze Pipeline ETL
(dados brutos) │
│ ┌──────┴──────┐
▼ ▼ ▼
🥈 Silver Limpeza Padronização
(dados tratados) & Tipagem & Regras
│
▼
🥇 Gold
(indicadores)
│
┌─────────┴─────────┐
▼ ▼
[API] [Dashboards]
(FastAPI) Web / Power BI / BI Tools
```


---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Função |
|--------|-----------|--------|
| Banco de dados | Supabase (PostgreSQL) | Armazenamento e acesso |
| ETL / Pipeline | Python + pandas | Transformações (Bronze → Gold) |
| API | FastAPI | Exposição dos dados |
| Visualização | JavaScript (Chart.js / Plotly) | Dashboard web |
| BI Externo | Power BI / Tableau / Looker | Consumo analítico |
| Deploy | Render / Vercel | Publicação da aplicação |

---

## 🗂️ Estrutura do Projeto

```
project-analytics-platform/
│
├── data/
│ ├── raw/ # Dataset original (não versionado)
│ ├── bronze/ # Dados brutos
│ ├── silver/ # Dados tratados
│ └── gold/ # Dados analíticos
│
├── ingestion/
│ └── ingest_csv.py # Ingestão inicial
│
├── pipeline/
│ ├── bronze_to_silver.py # Limpeza e padronização
│ └── silver_to_gold.py # Criação de métricas
│
├── api/
│ └── main.py # FastAPI endpoints
│
├── dashboard/
│ └── web/ # Frontend (JS)
│
├── docs/
│ ├── eda_insights.md # Análise exploratória
│ ├── architecture.md # Decisões técnicas
│ └── data_dictionary.md # Dicionário de dados
│
├── .env.example
├── requirements.txt
└── README.md

```


---

## 📊 Dataset

Dataset de **Gestão de Projetos (Kaggle)** contendo informações como:

- Datas de início e fim
- Status dos projetos
- Custos planejados vs reais
- Responsáveis (gestores)
- Indicadores operacionais

---

## 📈 Indicadores Monitorados

| Indicador | Descrição | Insight Gerado |
|-----------|-----------|----------------|
| **% Projetos Atrasados** | Projetos com end_date > planned_end | Eficiência operacional |
| **Variação de Custo (%)** | (Real - Planejado) / Planejado | Controle financeiro |
| **Duração Média** | Tempo médio de execução | Produtividade |
| **Taxa de Sucesso** | Projetos concluídos com sucesso | Qualidade da entrega |
| **Performance por Gestor** | KPIs por responsável | Gestão de equipes |

---

## 🔄 Pipeline de Dados

### 🥉 Bronze
- Armazena dados brutos
- Sem transformações
- Fonte única da verdade

---

### 🥈 Silver
- Limpeza de dados
- Conversão de tipos
- Padronização de status
- Tratamento de valores nulos

---

### 🥇 Gold
- Criação de métricas de negócio
- Dados prontos para análise
- Estrutura otimizada para consumo

---

## 🌐 API

A API permite acesso desacoplado aos dados:

```
GET /projects
GET /kpis
GET /projects/{id}
GET /performance
```


---

## 📊 Tipos de Análise

### 🔹 Visão Executiva
- KPIs estratégicos
- Visão consolidada dos projetos
- Análise de custos e prazos

---

### 🔹 Visão Operacional
- Status detalhado dos projetos
- Identificação de atrasos
- Análise por responsável

---

## 🤖 Uso de IA no Projeto

A IA é utilizada como:

- Copiloto de desenvolvimento
- Suporte na modelagem de dados
- Apoio na definição de KPIs
- Revisão de arquitetura e lógica

---

## 🚀 Como Executar

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/project-analytics-platform.git
cd project-analytics-platform

# 2. Ambiente virtual
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar pipeline
python ingestion/ingest_csv.py
python pipeline/bronze_to_silver.py
python pipeline/silver_to_gold.py

# 5. Rodar API
uvicorn api.main:app --reload

```
---

| Entrega              | Status                |
| -------------------- | --------------------- |
| Arquitetura Medalhão | ✅ Concluído           |
| Pipeline ETL         | 🔄 Em desenvolvimento |
| API (FastAPI)        | ⏳ Aguardando          |
| Dashboard Web        | ⏳ Aguardando          |
| Integração com BI    | ⏳ Aguardando          |
| Deploy               | ⏳ Aguardando          |


---

💼 Sobre o Projeto

Este projeto demonstra a capacidade de:

Construir pipelines de dados end-to-end
Aplicar arquitetura medalhão
Conectar dados a decisões de negócio
Criar soluções escaláveis e desacopladas

---

## 🚀 Autor

**Moisés Ribeiro**  
Analista de Dados, Projetos & Processos  
Lean Six Sigma | Python, R, SQL, Power BI  
Focado em Melhoria Contínua orientada a Dados

🔗 **LinkedIn:** https://www.linkedin.com/in/moisesrsjr/  
🧪 **Lab (Projetos e Experimentos):** https://github.com/moises-rb-lab  
💻 **Vitrine (Portfólio Principal):** https://github.com/moises-rb  
✍️ **Artigos e Insights:** https://medium.com/@moises.rsjr

---

📢 Destaque

“Mais do que analisar dados, este projeto demonstra a capacidade de construir uma solução completa de dados — da ingestão ao insight.”