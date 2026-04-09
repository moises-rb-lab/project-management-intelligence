import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
BASE_PATH   = Path(__file__).resolve().parents[2]
BRONZE_PATH = BASE_PATH / "data" / "risk" / "bronze"
SILVER_PATH = BASE_PATH / "data" / "risk" / "silver"
SOURCE_FILE = "project_risk_bronze.parquet"

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


def impute_tech_environment(df: pd.DataFrame) -> pd.DataFrame:
    """65% nulos — preenche com 'Unknown' para preservar a coluna."""
    before = df["Tech_Environment_Stability"].isna().sum()
    df["Tech_Environment_Stability"] = df["Tech_Environment_Stability"].fillna("Unknown")
    print(f"[OK] Tech_Environment_Stability — {before} nulos preenchidos com 'Unknown'")
    return df


def impute_by_group(df: pd.DataFrame) -> pd.DataFrame:
    """~20% nulos — preenche pela moda do Project_Type (mais preciso que moda global)."""
    cols = ["Change_Control_Maturity", "Risk_Management_Maturity"]

    for col in cols:
        before = df[col].isna().sum()

        # Moda por grupo
        group_mode = df.groupby("Project_Type")[col].transform(
            lambda x: x.fillna(x.mode()[0] if not x.mode().empty else "Unknown")
        )
        df[col] = df[col].fillna(group_mode)

        # Fallback global caso algum grupo fique sem moda
        global_mode = df[col].mode()[0]
        df[col] = df[col].fillna(global_mode)

        print(f"[OK] {col} — {before} nulos imputados por moda do grupo")

    return df


def standardize_strings(df: pd.DataFrame) -> pd.DataFrame:
    str_cols = df.select_dtypes(include="str").columns
    for col in str_cols:
        df[col] = df[col].str.strip().str.title()
    print(f"[OK] {len(str_cols)} colunas de texto padronizadas")
    return df


def save_silver(df: pd.DataFrame) -> None:
    SILVER_PATH.mkdir(parents=True, exist_ok=True)
    output_path = SILVER_PATH / "project_risk_silver.parquet"
    df.to_parquet(output_path, index=False)
    print(f"[SILVER] Arquivo salvo em: {output_path}")


# ─────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 50)
    print("  PIPELINE — Bronze → Silver (risk)")
    print("═" * 50)

    df = load_bronze(SOURCE_FILE)
    df = clean_column_names(df)
    df = impute_tech_environment(df)
    df = impute_by_group(df)
    df = standardize_strings(df)
    save_silver(df)

    print("═" * 50)
    print("  Pipeline concluído com sucesso!")
    print("═" * 50 + "\n")