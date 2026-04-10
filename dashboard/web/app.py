import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Project Analytics",
    page_icon="📊",
    layout="wide"
)

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch(endpoint: str, params: dict = {}) -> pd.DataFrame:
    try:
        response = requests.get(f"{API_BASE}{endpoint}", params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()["data"])
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        return pd.DataFrame()


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
st.sidebar.title("📊 Project Analytics")
dominio = st.sidebar.radio("Domínio", ["Management", "Risk"])


# ─────────────────────────────────────────
# DOMÍNIO — MANAGEMENT
# ─────────────────────────────────────────
if dominio == "Management":
    st.title("📁 Management Dashboard")
    st.caption("Visão estratégica para stakeholders")

    # ── Dados ──
    df_projects    = fetch("/management/projects")
    df_status      = fetch("/management/status")
    df_dept_region = fetch("/management/department-region")
    df_phase       = fetch("/management/phase-complexity")

    if df_projects.empty:
        st.warning("Sem dados disponíveis.")
        st.stop()

    # ── KPIs rápidos ──
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Projetos", len(df_projects))
    col2.metric("ROI Médio", f"{df_projects['roi'].mean():.2%}")
    col3.metric("Custo Total", f"R$ {df_projects['project_cost'].sum():,.0f}")
    col4.metric("Conclusão Média", f"{df_projects['completion_pct'].mean():.1f}%")

    st.divider()

    # ── Linha 1 ──
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Projetos por Status")
        fig = px.bar(
            df_status,
            x="status",
            y="total",
            color="status",
            text="total",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Distribuição por Complexidade")
        complexity = df_projects["complexity"].value_counts().reset_index()
        complexity.columns = ["complexity", "total"]
        fig = px.pie(
            complexity,
            names="complexity",
            values="total",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Linha 2 ──
    st.subheader("Custo e Benefício por Departamento")
    fig = px.bar(
        df_dept_region,
        x="department",
        y=["total_cost", "total_benefit"],
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"value": "Valor (R$)", "variable": "Métrica"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Linha 3 ──
    st.subheader("Heatmap — Fase vs Complexidade")
    if not df_phase.empty:
        pivot = df_phase.pivot_table(
            index="phase",
            columns="complexity",
            values="total_projects",
            fill_value=0
        )
        fig = px.imshow(
            pivot,
            color_continuous_scale="Blues",
            text_auto=True,
            labels={"color": "Projetos"}
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Tabela KPIs ──
    st.subheader("KPIs por Projeto")
    cols = ["project_name", "status", "completion_pct", "project_cost",
            "project_benefit", "roi", "duration_days"]
    st.dataframe(
        df_projects[cols].rename(columns={
            "project_name":   "Projeto",
            "status":         "Status",
            "completion_pct": "Conclusão %",
            "project_cost":   "Custo",
            "project_benefit":"Benefício",
            "roi":            "ROI",
            "duration_days":  "Duração (dias)"
        }),
        use_container_width=True
    )


# ─────────────────────────────────────────
# DOMÍNIO — RISK
# ─────────────────────────────────────────
elif dominio == "Risk":
    st.title("⚠️ Risk Dashboard")
    st.caption("Visão operacional para times e gestores de projeto")

    # ── Dados ──
    df_profile    = fetch("/risk/profile")
    df_by_type    = fetch("/risk/by-type")
    df_by_method  = fetch("/risk/by-methodology")
    df_factors    = fetch("/risk/factors")

    if df_profile.empty:
        st.warning("Sem dados disponíveis.")
        st.stop()

    # ── KPIs rápidos ──
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Projetos", len(df_profile))
    col2.metric("Complexidade Média", f"{df_profile['complexity_score'].mean():.2f}")
    col3.metric("Orçamento Médio", f"$ {df_profile['project_budget_usd'].mean():,.0f}")
    col4.metric("Incidentes Históricos Médios", f"{df_profile['historical_risk_incidents'].mean():.1f}")

    st.divider()

    # ── Linha 1 ──
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Projetos por Nível de Risco")
        risk_count = df_profile["risk_level"].value_counts().reset_index()
        risk_count.columns = ["risk_level", "total"]
        fig = px.bar(
            risk_count,
            x="risk_level",
            y="total",
            color="risk_level",
            text="total",
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Distribuição por Tipo de Projeto")
        fig = px.pie(
            df_by_type.groupby("project_type")["total"].sum().reset_index(),
            names="project_type",
            values="total",
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Linha 2 ──
    st.subheader("Complexidade Média por Metodologia e Experiência do Time")
    fig = px.bar(
        df_by_method,
        x="methodology_used",
        y="avg_complexity",
        color="team_experience_level",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Set1,
        labels={"avg_complexity": "Complexidade Média", "methodology_used": "Metodologia"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Linha 3 ──
    st.subheader("Fatores de Risco por Nível")
    st.dataframe(
        df_factors.rename(columns={
            "risk_level":               "Nível de Risco",
            "total":                    "Total",
            "avg_complexity":           "Complexidade Média",
            "avg_historical_incidents": "Incidentes Históricos",
            "avg_external_dependencies":"Dependências Externas",
            "avg_change_frequency":     "Frequência de Mudanças",
            "avg_team_turnover":        "Rotatividade do Time"
        }),
        use_container_width=True
    )

    # ── Tabela perfil ──
    st.subheader("Perfil de Risco por Projeto")
    cols = ["project_id", "project_type", "risk_level", "complexity_score",
            "team_size", "project_budget_usd", "methodology_used"]
    st.dataframe(
        df_profile[cols].rename(columns={
            "project_id":         "ID",
            "project_type":       "Tipo",
            "risk_level":         "Nível de Risco",
            "complexity_score":   "Complexidade",
            "team_size":          "Time",
            "project_budget_usd": "Orçamento (USD)",
            "methodology_used":   "Metodologia"
        }),
        use_container_width=True
    )