# 📌 Project Analytics — Resumo Estratégico

---

## 1️⃣ O que pretendemos fazer?

Construir uma **plataforma completa de analytics para gestão de projetos**, indo além de dashboards e contemplando:

- Ingestão de dados
- Pipeline ETL
- Arquitetura medalhão (Bronze, Silver, Gold)
- Exposição via API
- Consumo por dashboards web e ferramentas de BI

👉 Em resumo:  
**Transformar dados brutos em decisões estratégicas de negócio**

---

## 2️⃣ Como pretendemos fazer?

Através de uma abordagem estruturada, escalável e desacoplada:

- 📥 Ingestão de dados via CSV
- 🧱 Organização em camadas:
  - Bronze → dados brutos
  - Silver → dados tratados
  - Gold → dados analíticos (KPIs)
- 🔄 Pipeline ETL em Python
- 🌐 Exposição via API (FastAPI)
- 📊 Consumo via dashboards e ferramentas externas

👉 Seguindo princípios de:
- Engenharia de Dados
- Separação de responsabilidades
- Arquitetura moderna e escalável

---

## 3️⃣ O que utilizaremos para fazer?

### 🛠️ Stack Tecnológica

- **Python + Pandas** → ETL
- **PostgreSQL (Supabase)** → Banco de dados
- **FastAPI** → API
- **JavaScript (Chart.js / Plotly)** → Dashboard web
- **Power BI / Tableau / Looker** → Consumo analítico

---

### 🧱 Infraestrutura

- **Render** → Backend
- **Vercel** → Frontend
- **GitHub Codespaces** → Ambiente de desenvolvimento

---

### 📊 Dados

- Dataset de Gestão de Projetos (Kaggle)
- Possível enriquecimento com dataset de risco

---

## 4️⃣ Por que faremos?

Para resolver problemas reais de negócio:

- Falta de visibilidade sobre projetos
- Baixa previsibilidade de prazos
- Estouro de custos
- Decisões não orientadas a dados

---

E também para:

- Desenvolver visão analítica e arquitetural
- Conectar teoria com prática
- Construir um portfólio de alto nível

---

## 5️⃣ Qual objetivo pretendemos alcançar?

### 🎯 Objetivo técnico

- Construir pipelines de dados end-to-end
- Aplicar arquitetura medalhão
- Estruturar dados para análise
- Expor dados via API
- Criar soluções escaláveis

---

### 💼 Objetivo profissional

Ser capaz de afirmar:

> “Desenvolvi uma plataforma de analytics para gestão de projetos utilizando arquitetura medalhão, pipeline ETL em Python e dashboards interativos, permitindo integração com ferramentas de BI e apoiando decisões orientadas a dados.”

---

### 🚀 Objetivo estratégico

👉 Se posicionar como:

**Analista de Dados com visão de Engenharia e Arquitetura**

---

## 6️⃣ O que já foi feito?

### 🧱 Estrutura do Projeto Criada

```

project-analytics-platform/
│
├── data/
│ ├── raw/ # Dados brutos (datasets)
│ ├── bronze/ # Camada Bronze
│ ├── silver/ # Camada Silver
│ └── gold/ # Camada Gold
│
├── ingestion/
│ └── ingest_csv.py # Script de ingestão de dados
│
├── pipeline/
│ ├── bronze_to_silver.py # Pipeline de limpeza
│ └── silver_to_gold.py # Pipeline de métricas
│
├── api/
│ └── main.py # Estrutura inicial da API
│
├── dashboard/
│ └── web/ # Estrutura para frontend
│
├── docs/
│ ├── eda_insights.md # Documentação da análise exploratória
│ ├── architecture.md # Decisões arquiteturais
│ └── data_dictionary.md # Dicionário de dados
│
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore

```


---

### ⚙️ Ambiente configurado

- Ambiente virtual criado (`.venv`)
- Dependências instaladas:
  - pandas
  - fastapi
  - uvicorn
  - python-dotenv
  - psycopg2

---

### 📊 Ingestão de dados realizada

- Dois datasets carregados:
  - Dataset 1 → Gestão de Projetos (~99 linhas)
  - Dataset 2 → Dataset de Risco (~4000 linhas)

- Script de ingestão criado com:
  - leitura estruturada
  - validação de caminho
  - preview dos dados

---

### 🧠 Decisão estratégica tomada

- Dataset principal definido:
  👉 **Dataset de Gestão de Projetos**

- Dataset secundário:
  👉 **Reservado para evolução futura (análise de risco)**

---

## 7️⃣ O que recomendamos?

### 🧠 Evolução para Arquitetura Desacoplada

Para aumentar escalabilidade e maturidade do projeto, recomenda-se evoluir para:

---

### 🔹 Separação por repositórios

```

project-analytics-api/
project-analytics-frontend/
project-analytics-data/

```


---

### 🔹 Benefícios dessa abordagem

- 🔧 Manutenção isolada por camada
- 🚀 Deploy independente
- 🔄 Evolução sem impacto no todo
- 📦 Melhor organização do código
- 🌐 Integração facilitada com múltiplos consumidores

---

### 🔹 Modelo de comunicação

```

Frontend (Dashboard / BI)
↓
(HTTP)
↓
API (FastAPI)
↓
Banco de Dados (PostgreSQL)

```


---

### 🔹 Princípio-chave

👉 O frontend nunca acessa diretamente o banco  
👉 Toda comunicação passa pela API  

---

### 🔥 Resultado esperado

- Arquitetura próxima ao mercado real
- Maior flexibilidade tecnológica
- Projeto com nível profissional elevado

---

# 🚀 Conclusão

Este projeto não se limita à análise de dados, mas representa a construção de uma **plataforma completa de dados**, conectando:

- Engenharia
- Análise
- Arquitetura
- Negócio

---

> “Mais do que analisar dados, o objetivo é construir soluções que gerem impacto real.”