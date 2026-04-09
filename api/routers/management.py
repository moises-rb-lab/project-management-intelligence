import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
BASE_PATH = Path(__file__).resolve().parents[2]
GOLD_PATH = BASE_PATH / "data" / "management" / "gold"

router = APIRouter(prefix="/management", tags=["Management"])


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def load_gold(file_name: str) -> pd.DataFrame:
    path = GOLD_PATH / file_name
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {file_name}")
    return pd.read_parquet(path)


def df_to_json(df: pd.DataFrame) -> list:
    return df.where(pd.notnull(df), None).to_dict(orient="records")


# ─────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────
@router.get("/projects", summary="Lista todos os projetos com KPIs")
def get_projects(
    status: Optional[str]     = Query(None, description="Filtrar por status (ex: Completed)"),
    region: Optional[str]     = Query(None, description="Filtrar por região (ex: North)"),
    department: Optional[str] = Query(None, description="Filtrar por departamento"),
    complexity: Optional[str] = Query(None, description="Filtrar por complexidade (ex: High)"),
    year: Optional[int]       = Query(None, description="Filtrar por ano"),
):
    df = load_gold("projects_kpis.parquet")

    if status:
        df = df[df["Status"].str.title() == status.title()]
    if region:
        df = df[df["Region"].str.title() == region.title()]
    if department:
        df = df[df["Department"].str.title() == department.title()]
    if complexity:
        df = df[df["Complexity"].str.title() == complexity.title()]
    if year:
        df = df[df["Year"] == year]

    return {"total": len(df), "data": df_to_json(df)}


@router.get("/status", summary="Resumo de projetos por status")
def get_status_summary():
    df = load_gold("status_summary.parquet")
    return {"total": len(df), "data": df_to_json(df)}


@router.get("/department-region", summary="Custo e benefício por departamento e região")
def get_department_region(
    department: Optional[str] = Query(None, description="Filtrar por departamento"),
    region: Optional[str]     = Query(None, description="Filtrar por região"),
):
    df = load_gold("department_region.parquet")

    if department:
        df = df[df["Department"].str.title() == department.title()]
    if region:
        df = df[df["Region"].str.title() == region.title()]

    return {"total": len(df), "data": df_to_json(df)}


@router.get("/phase-complexity", summary="Distribuição por fase e complexidade")
def get_phase_complexity(
    phase: Optional[str]      = Query(None, description="Filtrar por fase"),
    complexity: Optional[str] = Query(None, description="Filtrar por complexidade"),
):
    df = load_gold("phase_complexity.parquet")

    if phase:
        df = df[df["Phase"].str.title() == phase.title()]
    if complexity:
        df = df[df["Complexity"].str.title() == complexity.title()]

    return {"total": len(df), "data": df_to_json(df)}