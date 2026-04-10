import os
import psycopg2
from dotenv import load_dotenv

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ─────────────────────────────────────────
# SQL — CRIAÇÃO DAS TABELAS
# ─────────────────────────────────────────
CREATE_TABLES_SQL = """
    CREATE TABLE IF NOT EXISTS risk_projects (
        id                              SERIAL PRIMARY KEY,
        project_id                      TEXT,
        project_type                    TEXT,
        team_size                       INTEGER,
        project_budget_usd              NUMERIC,
        estimated_timeline_months       INTEGER,
        complexity_score                NUMERIC,
        stakeholder_count               INTEGER,
        methodology_used                TEXT,
        team_experience_level           TEXT,
        past_similar_projects           INTEGER,
        external_dependencies_count     INTEGER,
        change_request_frequency        NUMERIC,
        project_phase                   TEXT,
        requirement_stability           TEXT,
        team_turnover_rate              NUMERIC,
        vendor_reliability_score        NUMERIC,
        historical_risk_incidents       INTEGER,
        communication_frequency         NUMERIC,
        regulatory_compliance_level     TEXT,
        technology_familiarity          TEXT,
        geographical_distribution       INTEGER,
        stakeholder_engagement_level    TEXT,
        schedule_pressure               NUMERIC,
        budget_utilization_rate         NUMERIC,
        executive_sponsorship           TEXT,
        funding_source                  TEXT,
        market_volatility               NUMERIC,
        integration_complexity          NUMERIC,
        resource_availability           NUMERIC,
        priority_level                  TEXT,
        organizational_change_frequency NUMERIC,
        cross_functional_dependencies   INTEGER,
        previous_delivery_success_rate  NUMERIC,
        technical_debt_level            NUMERIC,
        project_manager_experience      TEXT,
        org_process_maturity            TEXT,
        data_security_requirements      TEXT,
        key_stakeholder_availability    TEXT,
        tech_environment_stability      TEXT,
        contract_type                   TEXT,
        resource_contention_level       TEXT,
        industry_volatility             TEXT,
        client_experience_level         TEXT,
        change_control_maturity         TEXT,
        risk_management_maturity        TEXT,
        team_colocation                 TEXT,
        documentation_quality           TEXT,
        project_start_month             INTEGER,
        current_phase_duration_months   INTEGER,
        seasonal_risk_factor            NUMERIC,
        risk_level                      TEXT
    );
"""

# ─────────────────────────────────────────
# FUNÇÕES
# ─────────────────────────────────────────
def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("[OK] Conexão com o banco estabelecida")
        return conn
    except Exception as e:
        raise ConnectionError(f"Erro ao conectar ao banco: {e}")


def create_tables(conn) -> None:
    with conn.cursor() as cursor:
        cursor.execute(CREATE_TABLES_SQL)
        conn.commit()
        print("[OK] Tabela risk_projects criada (ou já existia)")


# ─────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 50)
    print("  BANCO — Criação de tabelas (risk)")
    print("═" * 50)

    conn = get_connection()

    try:
        create_tables(conn)
    finally:
        conn.close()
        print("[OK] Conexão encerrada")

    print("═" * 50 + "\n")