# 🏗️ Arquitetura da Plataforma — Project Analytics

---

## 📌 Visão Geral

Este projeto foi concebido como uma **plataforma moderna de dados**, com foco em:

- Escalabilidade
- Desacoplamento
- Reprodutibilidade
- Clareza entre camadas

A arquitetura segue o padrão de **Arquitetura Medalhão (Medallion Architecture)**, amplamente utilizado em soluções analíticas modernas.

---

## 🎯 Princípios Arquiteturais

A construção da solução é guiada pelos seguintes princípios:

### 1. 🔹 Separação de Responsabilidades
Cada camada possui uma função clara e isolada:
- Ingestão
- Processamento
- Exposição
- Consumo

---

### 2. 🔹 Desacoplamento
- O frontend não acessa diretamente o banco
- A API atua como camada intermediária
- Cada componente pode evoluir de forma independente

---

### 3. 🔹 Escalabilidade
A arquitetura permite:
- aumento de volume de dados
- inclusão de novas fontes
- expansão de métricas

---

### 4. 🔹 Reprodutibilidade
- Pipeline estruturado
- Código versionado
- Processos determinísticos

---

## 🧱 Arquitetura em Camadas

A solução é organizada em cinco principais camadas:

---

### 🥉 1. Camada Bronze (Raw Data)

**Objetivo:**
Armazenar os dados exatamente como foram recebidos.

**Características:**
- Sem transformações
- Fonte única da verdade
- Preserva histórico original

**Entrada:**
- Arquivos CSV

**Saída:**
- Dados brutos armazenados

---

### 🥈 2. Camada Silver (Clean Data)

**Objetivo:**
Transformar dados brutos em dados confiáveis.

**Processos realizados:**
- Limpeza de dados
- Tratamento de valores nulos
- Conversão de tipos (ex: datas)
- Padronização de categorias

**Resultado:**
- Dados consistentes e utilizáveis

---

### 🥇 3. Camada Gold (Business Data)

**Objetivo:**
Gerar valor de negócio a partir dos dados.

**Processos realizados:**
- Criação de métricas
- Cálculo de KPIs
- Agregações

**Exemplos de KPIs:**
- % de projetos atrasados
- Variação de custo
- Duração média
- Taxa de sucesso

---

### 🌐 4. Camada de API

**Objetivo:**
Expor os dados de forma padronizada e desacoplada.

**Tecnologia:**
- FastAPI

**Responsabilidades:**
- Disponibilizar endpoints
- Servir dados para múltiplos consumidores
- Controlar acesso aos dados

---

### 📊 5. Camada de Consumo (Frontend / BI)

**Objetivo:**
Permitir a análise e visualização dos dados.

**Consumidores possíveis:**
- Dashboard web (JavaScript)
- Ferramentas de BI (Power BI, Tableau, Looker)

---

## 🔄 Fluxo de Dados

```
CSV (Entrada)
↓
Bronze (Raw)
↓
Silver (Clean)
↓
Gold (Business)
↓
API (FastAPI)
↓
Dashboards / BI

```
---

## 🧠 Pipeline ETL

O pipeline segue o modelo clássico:

### Extract
- Leitura de arquivos CSV

---

### Transform
- Limpeza
- Padronização
- Enriquecimento
- Criação de métricas

---

### Load
- Armazenamento estruturado
- Persistência em banco (PostgreSQL)

---

## 🗂️ Organização do Código
```
ingestion/ → Entrada de dados
pipeline/ → Transformações (ETL)
data/ → Armazenamento por camada
api/ → Exposição de dados
dashboard/ → Visualização
docs/ → Documentação
```

---

## 🔌 Integração entre Componentes

A comunicação entre as camadas segue o padrão:
```
Frontend / BI
↓ (HTTP)
API (FastAPI)
↓
Banco de Dados (PostgreSQL)
```

---

## 🚀 Evolução Arquitetural (Futuro)

Para maior maturidade, recomenda-se evoluir para:

### 🔹 Repositórios desacoplados
```
project-analytics-data/
project-analytics-api/
project-analytics-frontend/
```

---

### 🔹 Benefícios

- Deploy independente
- Escalabilidade por camada
- Facilidade de manutenção
- Evolução tecnológica isolada

---

## ⚖️ Decisões Arquiteturais

| Decisão | Justificativa |
|--------|--------------|
| Uso de arquitetura medalhão | Organização e escalabilidade |
| API como camada intermediária | Desacoplamento |
| Python + Pandas | Simplicidade e poder analítico |
| PostgreSQL | Robustez e padrão de mercado |
| Separação por diretórios | Clareza estrutural |

---

## 🚫 Trade-offs

| Escolha | Impacto |
|--------|--------|
| Uso de CSV inicial | Simplicidade, porém sem ingestão em tempo real |
| Não uso de streaming | Menor complexidade inicial |
| Monorepo inicial | Simplicidade, menor isolamento |

---

## 🎯 Conclusão

A arquitetura foi projetada para:

- suportar crescimento
- facilitar manutenção
- permitir evolução contínua

---

> “Uma boa arquitetura não é a mais complexa, mas a que permite evoluir sem quebrar.”