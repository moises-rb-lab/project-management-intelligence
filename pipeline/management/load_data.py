import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
load_dotenv()

client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

BASE_PATH   = Path(__file__).resolve().parents[2]
SILVER_PATH = BASE_PATH / "data" / "management" / "silver"
SOURCE_FILE = "project_management_silver.parquet"

# ─────────────────────────────────────────
# FUNÇÕES
# ─────────────────────────────────────────
def load_silver() -> pd.DataFrame:
    path = SILVER_PATH / SOURCE_FILE
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    df = pd.read_parquet(path)
    print(f"[SILVER] {len(df)} linhas carregadas")
    return df


def prepare(df: pd.DataFrame) -> list:
    """Converte o DataFrame para lista de dicts compatível com o Supabase."""
    df = df.rename(columns={
        "Project Name":        "project_name",
        "Project Description": "project_description",
        "Project Type":        "project_type",
        "Project Manager":     "project_manager",
        "Region":              "region",
        "Department":          "department",
        "Project Cost":        "project_cost",
        "Project Benefit":     "project_benefit",
        "Complexity":          "complexity",
        "Status":              "status",
        "Completion%":         "completion_pct",
        "Phase":               "phase",
        "Year":                "year",
        "Month":               "month",
        "Start Date":          "start_date",
        "End Date":            "end_date",
    })

    # Converte datas para string (o Supabase REST API espera ISO format)
    df["start_date"] = df["start_date"].dt.strftime("%Y-%m-%d")
    df["end_date"]   = df["end_date"].dt.strftime("%Y-%m-%d")

    # Converte para lista de dicts
    records = df.where(pd.notnull(df), None).to_dict(orient="records")
    print(f"[OK] {len(records)} registros preparados para inserção")
    return records


def insert(records: list) -> None:
    """Insere em lotes de 50 para evitar timeout."""
    batch_size = 50
    total      = len(records)
    inserted   = 0

    for i in range(0, total, batch_size):
        batch = records[i:i + batch_size]
        client.table("mgmt_projects").insert(batch).execute()
        inserted += len(batch)
        print(f"[OK] Inseridos {inserted}/{total} registros")

    print(f"[BANCO] Carga concluída — {inserted} registros inseridos")

# ─────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 50)
    print("  BANCO — Carga de dados (management)")
    print("═" * 50)

    df      = load_silver()
    records = prepare(df)
    insert(records)

    print("═" * 50 + "\n")