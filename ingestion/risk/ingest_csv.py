import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
BASE_PATH   = Path(__file__).resolve().parents[2]
RAW_PATH    = BASE_PATH / "data" / "raw"
BRONZE_PATH = BASE_PATH / "data" / "risk" / "bronze"
SOURCE_FILE = "project_risk_raw_dataset.csv"
OUTPUT_FILE = "project_risk_bronze.parquet"

# ─────────────────────────────────────────
# FUNÇÕES
# ─────────────────────────────────────────
def load_csv(file_name: str) -> pd.DataFrame:
    file_path = RAW_PATH / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df = pd.read_csv(file_path)
    print(f"[RAW] {len(df)} linhas carregadas de '{file_name}'")
    return df


def validate(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Dataset vazio — ingestão abortada.")
    print(f"[OK] Validação passou — {len(df)} linhas, {len(df.columns)} colunas")


def save_bronze(df: pd.DataFrame) -> None:
    BRONZE_PATH.mkdir(parents=True, exist_ok=True)
    output_path = BRONZE_PATH / OUTPUT_FILE
    df.to_parquet(output_path, index=False)
    print(f"[BRONZE] Salvo: {output_path}")


# ─────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 50)
    print("  INGESTÃO — Raw → Bronze (risk)")
    print("═" * 50)

    df = load_csv(SOURCE_FILE)
    validate(df)
    save_bronze(df)

    print("═" * 50)
    print("  Ingestão concluída com sucesso!")
    print("═" * 50 + "\n")