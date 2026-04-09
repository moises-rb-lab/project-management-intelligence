import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
BASE_PATH   = Path(__file__).resolve().parents[2]
SILVER_PATH = BASE_PATH / "data" / "management" / "silver"
GOLD_PATH   = BASE_PATH / "data" / "management" / "gold"
SOURCE_FILE = "project_management_silver.parquet"

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


def build_projects_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """ROI e duração por projeto — visão individual."""
    gold = df.copy()

    gold["ROI"] = ((gold["Project Benefit"] - gold["Project Cost"]) / gold["Project Cost"]).round(4)
    gold["Duration Days"] = (gold["End Date"] - gold["Start Date"]).dt.days

    cols = [
        "Project Name", "Project Type", "Department", "Region",
        "Status", "Phase", "Complexity", "Completion%",
        "Project Cost", "Project Benefit", "ROI",
        "Start Date", "End Date", "Duration Days", "Year", "Month"
    ]
    print("[OK] KPIs por projeto calculados (ROI + Duração)")
    return gold[cols]


def build_status_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Distribuição de status — visão executiva."""
    summary = (
        df.groupby("Status")
        .agg(
            Total=("Project Name", "count"),
            Avg_Completion=("Completion%", "mean"),
            Avg_Cost=("Project Cost", "mean"),
            Total_Cost=("Project Cost", "sum"),
        )
        .round(2)
        .reset_index()
    )
    summary["Pct_Projects"] = (summary["Total"] / summary["Total"].sum() * 100).round(1)
    print("[OK] Resumo por status calculado")
    return summary


def build_department_region(df: pd.DataFrame) -> pd.DataFrame:
    """Custo e benefício agregados por Departamento e Região."""
    agg = (
        df.groupby(["Department", "Region"])
        .agg(
            Total_Projects=("Project Name", "count"),
            Total_Cost=("Project Cost", "sum"),
            Total_Benefit=("Project Benefit", "sum"),
            Avg_ROI=("ROI" if "ROI" in df.columns else "Project Cost", "mean"),
        )
        .round(2)
        .reset_index()
    )
    agg["Net_Value"] = agg["Total_Benefit"] - agg["Total_Cost"]
    print("[OK] Agregação por Departamento e Região calculada")
    return agg


def build_phase_complexity(df: pd.DataFrame) -> pd.DataFrame:
    """Distribuição por fase e complexidade."""
    agg = (
        df.groupby(["Phase", "Complexity"])
        .agg(
            Total_Projects=("Project Name", "count"),
            Avg_Completion=("Completion%", "mean"),
            Avg_Cost=("Project Cost", "mean"),
        )
        .round(2)
        .reset_index()
    )
    print("[OK] Distribuição por fase e complexidade calculada")
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
    print("  PIPELINE — Silver → Gold (management)")
    print("═" * 50)

    df = load_silver(SOURCE_FILE)

    projects   = build_projects_kpis(df)
    status     = build_status_summary(projects)
    dept_region = build_department_region(projects)
    phase_complexity = build_phase_complexity(projects)

    save_gold(projects,        "projects_kpis.parquet")
    save_gold(status,          "status_summary.parquet")
    save_gold(dept_region,     "department_region.parquet")
    save_gold(phase_complexity,"phase_complexity.parquet")

    print("═" * 50)
    print("  Pipeline concluído com sucesso!")
    print("═" * 50 + "\n")