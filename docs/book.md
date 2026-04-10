# 📘 Project Book — Project Management Intelligence Platform

> *"Mais do que analisar dados, o objetivo é construir soluções que gerem impacto real."*

---

## 1. Visão Geral

Este documento registra as decisões técnicas, desafios enfrentados e soluções aplicadas na construção da **Project Management Intelligence Platform** — uma plataforma completa de analytics para gestão de projetos.

O projeto foi concebido para ir além de dashboards superficiais, contemplando toda a jornada do dado: da ingestão bruta até a exposição via API e consumo por dashboards interativos.

**Posicionamento:** Analista de Dados com visão de Engenharia — conectando análise, engenharia e arquitetura em um produto orientado a decisões de negócio.

---

## 2. O Problema de Negócio

Organizações que gerenciam múltiplos projetos simultaneamente enfrentam desafios recorrentes:

- **Falta de visibilidade** sobre o status real dos projetos
- **Baixa previsibilidade de prazos** — projetos que estouram cronograma sem sinal de alerta antecipado
- **Estouro de custos** sem rastreabilidade clara
- **Decisões não orientadas a dados** — gestores dependendo de relatórios manuais e planilhas desatualizadas
- **Ausência de análise de risco estruturada** — projetos iniciados sem avaliação prévia de complexidade e exposição

A plataforma foi construída para resolver esses problemas, transformando dados brutos em decisões estratégicas de negócio.

---

## 3. Arquitetura da Solução

A solução adota a **Arquitetura Medalhão** — padrão consolidado no mercado de engenharia de dados — organizada em camadas com responsabilidades distintas:

```
Raw (CSV)
  ↓  Ingestão
Bronze (Parquet — dado bruto preservado)
  ↓  Limpeza e padronização
Silver (Parquet + PostgreSQL — dado tratado e tipado)
  ↓  Agregação e cálculo de KPIs
Gold (Views SQL — dados analíticos prontos para consumo)
  ↓  Exposição
API (FastAPI)
  ↓  Consumo
Dashboard (Streamlit → JavaScript/Vercel)
```

### Separação por Domínios

Uma decisão arquitetural central foi tratar os dois datasets como **domínios independentes**, cada um com sua própria audiência e propósito:

| Domínio | Audiência | Perguntas que responde |
|---|---|---|
| **Management** | Stakeholders e Diretoria | ROI por projeto, status, custo por departamento, prazo |
| **Risk** | Times e Gestores de Projeto | Nível de risco, fatores de risco, metodologia vs complexidade |

Essa separação garante que cada audiência receba exatamente o que precisa — sem ruído e sem complexidade desnecessária.

### Modelo de Comunicação

```
Dashboard / BI
      ↓
   (HTTP)
      ↓
 API (FastAPI)
      ↓
Banco (Supabase/PostgreSQL)
```

**Princípio-chave:** o frontend nunca acessa diretamente o banco. Toda comunicação passa pela API — padrão de mercado que garante segurança, rastreabilidade e flexibilidade para evoluir cada camada de forma independente.

---

## 4. Decisões Técnicas e Justificativas

### 4.1 Formato de armazenamento: CSV vs Parquet

**Decisão:** CSV permanece apenas na camada Raw. A partir da Bronze, todos os arquivos são armazenados em **Parquet**.

**Justificativa:** CSV é como um caderno de papel — qualquer um abre, mas fica pesado e lento conforme cresce. O Parquet é um formato colunar compactado, com leitura muito mais rápida, menor consumo de espaço e suporte nativo em Pandas, Spark e ferramentas de BI. É o padrão do mercado em pipelines de dados modernos.

### 4.2 Duas formas de conexão com o banco

**Decisão:** O projeto utiliza intencionalmente duas bibliotecas distintas para comunicação com o banco.

| Biblioteca | Uso | Motivo |
|---|---|---|
| `psycopg2` | Scripts de administração (criar tabelas, views) | Conexão direta — executa SQL arbitrário |
| `supabase-py` | API — leitura de dados | Cliente REST — mais seguro para exposição de dados |

**Justificativa:** O `supabase-py` é um cliente REST — ele é ideal para operações de leitura e escrita no dia a dia, mas não executa SQL arbitrário. Para scripts de administração, como criação de tabelas e views, é necessário o `psycopg2` com conexão direta via `postgresql://`. Essa separação é comum no mercado: você não usa o mesmo tipo de conexão para tudo.

### 4.3 Views SQL como camada Gold no banco

**Decisão:** A camada Gold não é uma tabela física, mas uma **view SQL** no banco de dados.

**Justificativa:** Views são calculadas em tempo de execução sobre os dados da Silver. Isso garante que os KPIs estejam sempre atualizados sem necessidade de reprocessamento manual. Quando os dados da Silver são atualizados, as views refletem automaticamente as mudanças.

### 4.4 Domínios separados desde a Bronze

**Decisão:** Cada domínio possui seu próprio pipeline completo e independente.

**Justificativa:** Separar os domínios desde o início garante manutenção isolada, evolução independente e deploy sem impacto entre as camadas. Um bug no pipeline de `risk` não afeta o pipeline de `management`.

---

## 5. Desafios Enfrentados e Soluções

### 5.1 Incompatibilidade com Python 3.14

**Problema:** O ambiente foi inicialmente configurado com Python 3.14 — versão recém-lançada. A maioria das bibliotecas do ecossistema de dados ainda não possuía wheels pré-compilados para essa versão, causando falhas na instalação do `supabase` e dependências relacionadas.

**Análise:** Python 3.14 é muito recente para uso em projetos com dependências de terceiros. O ecossistema leva meses para acompanhar versões novas.

**Solução aplicada:** Recriação do ambiente virtual com **Python 3.11** — versão LTS com suporte total a todas as bibliotecas utilizadas no projeto.

**Aprendizado:** Em projetos de dados, estabilidade é mais importante que novidade. Versões LTS são a escolha certa para ambientes de desenvolvimento e produção.

---

### 5.2 Colunas nulas no dataset de risco

**Problema:** O dataset `project_risk_raw_dataset.csv` apresentava três colunas com valores ausentes significativos:

| Coluna | Nulos | % |
|---|---|---|
| `Tech_Environment_Stability` | 2.619 | 65,5% |
| `Change_Control_Maturity` | 780 | 19,5% |
| `Risk_Management_Maturity` | 791 | 19,8% |

**Análise das alternativas:**

Para `Tech_Environment_Stability` (65,5% nulos):
- **Remover a coluna** → perde informação potencial
- **Moda global** → distorce a distribuição real com 65% de dados inventados
- **Imputação por modelo (KNN)** → complexo e impreciso com tanta ausência
- **Preencher com `'Unknown'`** → preserva a coluna sem inventar dados

Para `Change_Control_Maturity` e `Risk_Management_Maturity` (~20% nulos):
- **Moda global** → ignora contexto do projeto
- **`'Unknown'`** → perde a informação dos 80% válidos
- **Imputação por grupo (`Project_Type`)** → mais precisa que moda global, pois projetos do mesmo tipo tendem a ter maturidade similar

**Soluções aplicadas:**
- `Tech_Environment_Stability` → preenchida com `'Unknown'` (65% de nulos não permite imputação confiável)
- `Change_Control_Maturity` e `Risk_Management_Maturity` → imputação pela **moda do grupo por `Project_Type`**, com fallback para moda global quando o grupo não possui moda

**Justificativa:** A imputação por grupo é muito mais precisa que a moda global porque respeita o contexto do dado. Um projeto de `Construction` provavelmente tem maturidade de controle diferente de um projeto de `IT`.

---

### 5.3 Supabase-py vs psycopg2

**Problema:** A tentativa inicial de usar o `supabase-py` para criação de tabelas falhou — o cliente REST não executa SQL arbitrário.

**Análise:** O `supabase-py` é um cliente REST que abstrai operações de CRUD via endpoints HTTP. Ele não é uma conexão direta ao banco e, portanto, não suporta DDL (Data Definition Language) como `CREATE TABLE`.

**Solução aplicada:** Separação intencional das ferramentas:
- `psycopg2` com `DATABASE_URL` para scripts de administração (DDL)
- `supabase-py` para a API (DML — leitura e escrita de dados)

Essa separação resultou em uma arquitetura mais madura e próxima do mercado real.

---

## 6. Stack Tecnológica

### Pipeline de Dados
| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal |
| Pandas | Transformações ETL |
| PyArrow | Leitura e escrita de Parquet |

### Banco de Dados
| Tecnologia | Uso |
|---|---|
| PostgreSQL (Supabase) | Banco de dados principal |
| psycopg2 | Conexão direta para DDL |
| supabase-py | Cliente REST para a API |

### API
| Tecnologia | Uso |
|---|---|
| FastAPI | Framework da API |
| Uvicorn | Servidor ASGI |
| python-dotenv | Gerenciamento de variáveis de ambiente |

### Frontend e Prototipagem
| Tecnologia | Uso |
|---|---|
| Streamlit | Prototipagem do dashboard |
| Plotly | Visualizações interativas |
| JavaScript + Chart.js | Frontend final (em desenvolvimento) |

### Infraestrutura
| Tecnologia | Uso |
|---|---|
| Render | Deploy da API |
| Vercel | Deploy do frontend |
| GitHub | Controle de versão |
| GitHub Codespaces | Ambiente de desenvolvimento |

---

## 7. Pipeline de Dados

### Estrutura de diretórios

```
project-management-intelligence/
│
├── data/
│   ├── raw/                  ← Datasets originais (CSV)
│   ├── management/
│   │   ├── bronze/           ← Dado bruto preservado (Parquet)
│   │   ├── silver/           ← Dado limpo e tipado (Parquet + PostgreSQL)
│   │   └── gold/             ← KPIs (Views SQL no banco)
│   └── risk/
│       ├── bronze/
│       ├── silver/
│       └── gold/
│
├── ingestion/
│   ├── management/
│   │   └── ingest_csv.py     ← Raw → Bronze
│   └── risk/
│       └── ingest_csv.py
│
├── pipeline/
│   ├── management/
│   │   ├── bronze_to_silver.py
│   │   ├── silver_to_gold.py
│   │   ├── create_tables.py  ← DDL via psycopg2
│   │   └── load_data.py      ← Carga via supabase-py
│   └── risk/
│       ├── bronze_to_silver.py
│       ├── silver_to_gold.py
│       ├── create_tables.py
│       └── load_data.py
│
├── api/
│   ├── main.py
│   └── routers/
│       ├── management.py
│       └── risk.py
│
└── dashboard/
    └── web/
        └── app.py            ← Protótipo Streamlit
```

### Ordem de execução

```bash
# Domínio Management
python ingestion/management/ingest_csv.py
python pipeline/management/bronze_to_silver.py
python pipeline/management/silver_to_gold.py
python pipeline/management/create_tables.py
python pipeline/management/load_data.py

# Domínio Risk
python ingestion/risk/ingest_csv.py
python pipeline/risk/bronze_to_silver.py
python pipeline/risk/silver_to_gold.py
python pipeline/risk/create_tables.py
python pipeline/risk/load_data.py
```

---

## 8. API

A API expõe os dados da camada Gold via endpoints REST, organizados por domínio. Todos os endpoints aceitam filtros opcionais via query parameters.

### Endpoints — Management

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/management/projects` | Projetos com KPIs (ROI, duração) |
| GET | `/management/status` | Resumo por status |
| GET | `/management/department-region` | Custo e benefício por departamento e região |
| GET | `/management/phase-complexity` | Distribuição por fase e complexidade |

### Endpoints — Risk

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/risk/profile` | Perfil de risco por projeto |
| GET | `/risk/by-type` | Distribuição de risco por tipo de projeto |
| GET | `/risk/by-methodology` | Risco por metodologia e experiência do time |
| GET | `/risk/factors` | Fatores de risco por nível |

### Exemplo de uso com filtros

```
GET /management/projects?status=Completed&region=North&complexity=High
GET /risk/profile?risk_level=High&project_type=It
```

A documentação interativa completa está disponível via Swagger UI em `/docs`.

---

## 9. KPIs Gerados

### Domínio Management

| KPI | Descrição |
|---|---|
| ROI por projeto | `(Benefício - Custo) / Custo` |
| Duração real | `End Date - Start Date` em dias |
| % de conclusão | Completion% por projeto |
| Custo e benefício total | Agregado por departamento e região |
| Valor líquido | `Benefício total - Custo total` por departamento |
| Distribuição por fase e complexidade | Quantidade de projetos por combinação |

### Domínio Risk

| KPI | Descrição |
|---|---|
| Nível de risco | Classificação por projeto (Low / Medium / High) |
| Complexidade média | Por tipo de projeto e metodologia |
| Rotatividade do time | Taxa média por nível de risco |
| Incidentes históricos | Média por nível de risco |
| Pressão de prazo | Schedule pressure por metodologia |
| Utilização de orçamento | Budget utilization rate por grupo |

---

## 10. Próximos Passos

- [ ] Deploy da API no **Render**
- [ ] Construção do frontend em **JavaScript** (Chart.js / Plotly.js)
- [ ] Deploy do frontend no **Vercel**
- [ ] Pipeline do domínio **Risk** completo no banco
- [ ] Implementação de **autenticação** na API (JWT)
- [ ] **Agendamento** do pipeline ETL (Airflow ou cron job)
- [ ] Expansão do domínio Risk com **análise preditiva**

---

## 11. Conclusão

Este projeto representa mais do que uma análise de dados — é a construção de uma **plataforma completa de dados**, conectando engenharia, análise, arquitetura e negócio.

Cada decisão técnica foi tomada com critério e justificativa — desde a escolha do formato Parquet até a separação entre `psycopg2` e `supabase-py`. Cada desafio foi documentado com as alternativas analisadas e a solução escolhida.

O resultado é um portfólio que demonstra não apenas capacidade técnica, mas **visão de produto e maturidade arquitetural** — posicionando o autor como um Analista de Dados com visão de Engenharia, capaz de construir soluções escaláveis e orientadas a impacto real.

---

*Documentação gerada ao longo do desenvolvimento do projeto — abril de 2026.*