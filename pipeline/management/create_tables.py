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
    CREATE TABLE IF NOT EXISTS mgmt_projects (
        id                  SERIAL PRIMARY KEY,
        project_name        TEXT,
        project_description TEXT,
        project_type        TEXT,
        project_manager     TEXT,
        region              TEXT,
        department          TEXT,
        project_cost        NUMERIC,
        project_benefit     NUMERIC,
        complexity          TEXT,
        status              TEXT,
        completion_pct      NUMERIC,
        phase               TEXT,
        year                INTEGER,
        month               INTEGER,
        start_date          DATE,
        end_date            DATE
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
        print("[OK] Tabela mgmt_projects criada (ou já existia)")


# ─────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 50)
    print("  BANCO — Criação de tabelas (management)")
    print("═" * 50)

    conn = get_connection()

    try:
        create_tables(conn)
    finally:
        conn.close()
        print("[OK] Conexão encerrada")

    print("═" * 50 + "\n")