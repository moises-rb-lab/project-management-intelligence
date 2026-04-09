import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
BASE_PATH   = Path(__file__).resolve().parents[2]
BRONZE_PATH = BASE_PATH / "data" / "management" / "bronze"
SILVER_PATH = BASE_PATH / "data" / "management" / "silver"
SOURCE_FILE = "project_management_bronze.parquet"

# ─────────────────────────────────────────
# FUNÇÕES DE TRANSFORMAÇÃO
# ─────────────────────────────────────────
def load_bronze(file_name: str) -> pd.DataFrame:
    file_path = BRONZE_PATH / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df = pd.read_parquet(file_path)
    print(f"[BRONZE] {len(df)} linhas carregadas")
    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()
    print("[OK] Nomes de colunas limpos")
    return df


def convert_currency(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["Project Cost", "Project Benefit"]:
        df[col] = (
            df[col]
            .str.replace(",", "", regex=False)
            .str.strip()
            .astype(float)
        )
    print("[OK] Colunas de moeda convertidas para float")
    return df


def convert_completion(df: pd.DataFrame) -> pd.DataFrame:
    df["Completion%"] = (
        df["Completion%"]
        .str.replace("%", "", regex=False)
        .str.strip()
        .astype(float)
    )
    print("[OK] Completion% convertido para float")
    return df


def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["Start Date", "End Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    print("[OK] Datas convertidas para datetime")
    return df


def standardize_strings(df: pd.DataFrame) -> pd.DataFrame:
    str_cols = df.select_dtypes(include="str").columns
    for col in str_cols:
        df[col] = df[col].str.strip().str.title()
    print(f"[OK] {len(str_cols)} colunas de texto padronizadas")
    return df


def save_silver(df: pd.DataFrame) -> None:
    SILVER_PATH.mkdir(parents=True, exist_ok=True)
    output_path = SILVER_PATH / "project_management_silver.parquet"
    df.to_parquet(output_path, index=False)
    print(f"[SILVER] Arquivo salvo em: {output_path}")


# ─────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 50)
    print("  PIPELINE — Bronze → Silver (management)")
    print("═" * 50)

    df = load_bronze(SOURCE_FILE)
    df = clean_column_names(df)
    df = convert_currency(df)
    df = convert_completion(df)
    df = convert_dates(df)
    df = standardize_strings(df)
    save_silver(df)

    print("═" * 50)
    print("  Pipeline concluído com sucesso!")
    print("═" * 50 + "\n")