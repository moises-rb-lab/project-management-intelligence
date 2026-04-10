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
SILVER_PATH = BASE_PATH / "data" / "risk" / "silver"
SOURCE_FILE = "project_risk_silver.parquet"

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
    df.columns = [col.lower() for col in df.columns]
    records = df.where(pd.notnull(df), None).to_dict(orient="records")
    print(f"[OK] {len(records)} registros preparados para inserção")
    return records


def insert(records: list) -> None:
    batch_size = 100
    total      = len(records)
    inserted   = 0

    for i in range(0, total, batch_size):
        batch = records[i:i + batch_size]
        client.table("risk_projects").insert(batch).execute()
        inserted += len(batch)
        print(f"[OK] Inseridos {inserted}/{total} registros")

    print(f"[BANCO] Carga concluída — {inserted} registros inseridos")


# ─────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 50)
    print("  BANCO — Carga de dados (risk)")
    print("═" * 50)

    df      = load_silver()
    records = prepare(df)
    insert(records)

    print("═" * 50 + "\n")