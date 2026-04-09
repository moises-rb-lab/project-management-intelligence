import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
BASE_PATH   = Path(__file__).resolve().parents[2]
SILVER_PATH = BASE_PATH / "data" / "risk" / "silver"
GOLD_PATH   = BASE_PATH / "data" / "risk" / "gold"
SOURCE_FILE = "project_risk_silver.parquet"

# ─────────────────────────────────────────
# FUNÇÕES DE KPI
# ─────────────────────────────────────────
def load_silver(file_name: str) -> pd.DataFrame:
    file_path = SILVER_PATH / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    df = pd.read_parquet(file_path)
    print(f"[SILVER] {len(df)} linhas carregadas")
    return df


def build_risk_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Perfil de risco por projeto — visão individual."""
    cols = [
        "Project_ID", "Project_Type", "Risk_Level", "Complexity_Score",
        "Team_Size", "Project_Budget_USD", "Estimated_Timeline_Months",
        "Team_Experience_Level", "Methodology_Used", "Project_Phase",
        "Budget_Utilization_Rate", "Schedule_Pressure", "Team_Turnover_Rate",
        "Historical_Risk_Incidents", "Tech_Environment_Stability",
        "Change_Control_Maturity", "Risk_Management_Maturity"
    ]
    print("[OK] Perfil de risco por projeto gerado")
    return df[cols].copy()


def build_risk_by_type(df: pd.DataFrame) -> pd.DataFrame:
    """Distribuição de risco por tipo de projeto."""
    agg = (
        df.groupby(["Project_Type", "Risk_Level"])
        .agg(
            Total=("Project_ID", "count"),
            Avg_Complexity=("Complexity_Score", "mean"),
            Avg_Budget=("Project_Budget_USD", "mean"),
            Avg_Timeline=("Estimated_Timeline_Months", "mean"),
        )
        .round(2)
        .reset_index()
    )
    print("[OK] Distribuição de risco por tipo de projeto gerada")
    return agg


def build_risk_by_methodology(df: pd.DataFrame) -> pd.DataFrame:
    """Risco médio por metodologia e experiência do time."""
    agg = (
        df.groupby(["Methodology_Used", "Team_Experience_Level"])
        .agg(
            Total=("Project_ID", "count"),
            Avg_Complexity=("Complexity_Score", "mean"),
            Avg_Turnover=("Team_Turnover_Rate", "mean"),
            Avg_Schedule_Pressure=("Schedule_Pressure", "mean"),
            Avg_Budget_Utilization=("Budget_Utilization_Rate", "mean"),
        )
        .round(2)
        .reset_index()
    )
    print("[OK] Risco por metodologia e experiência do time gerado")
    return agg


def build_risk_factors_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Resumo dos principais fatores de risco por nível de risco."""
    agg = (
        df.groupby("Risk_Level")
        .agg(
            Total=("Project_ID", "count"),
            Avg_Complexity=("Complexity_Score", "mean"),
            Avg_Historical_Incidents=("Historical_Risk_Incidents", "mean"),
            Avg_External_Dependencies=("External_Dependencies_Count", "mean"),
            Avg_Change_Frequency=("Change_Request_Frequency", "mean"),
            Avg_Team_Turnover=("Team_Turnover_Rate", "mean"),
        )
        .round(2)
        .reset_index()
    )
    print("[OK] Resumo de fatores de risco por nível gerado")
    return agg


def save_gold(df: pd.DataFrame, file_name: str) -> None:
    GOLD_PATH.mkdir(parents=True, exist_ok=True)
    output_path = GOLD_PATH / file_name
    df.to_parquet(output_path, index=False)
    print(f"[GOLD] Salvo: {output_path.name}")


# ─────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 50)
    print("  PIPELINE — Silver → Gold (risk)")
    print("═" * 50)

    df = load_silver(SOURCE_FILE)

    risk_profile     = build_risk_profile(df)
    risk_by_type     = build_risk_by_type(df)
    risk_by_method   = build_risk_by_methodology(df)
    risk_factors     = build_risk_factors_summary(df)

    save_gold(risk_profile,   "risk_profile.parquet")
    save_gold(risk_by_type,   "risk_by_type.parquet")
    save_gold(risk_by_method, "risk_by_methodology.parquet")
    save_gold(risk_factors,   "risk_factors_summary.parquet")

    print("═" * 50)
    print("  Pipeline concluído com sucesso!")
    print("═" * 50 + "\n")