import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
BASE_PATH = Path(__file__).resolve().parents[2]
GOLD_PATH = BASE_PATH / "data" / "risk" / "gold"

router = APIRouter(prefix="/risk", tags=["Risk"])


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
@router.get("/profile", summary="Perfil de risco por projeto")
def get_risk_profile(
    risk_level: Optional[str]        = Query(None, description="Filtrar por nível de risco (ex: High)"),
    project_type: Optional[str]      = Query(None, description="Filtrar por tipo de projeto (ex: It)"),
    project_phase: Optional[str]     = Query(None, description="Filtrar por fase (ex: Planning)"),
    experience_level: Optional[str]  = Query(None, description="Filtrar por experiência do time (ex: Senior)"),
):
    df = load_gold("risk_profile.parquet")

    if risk_level:
        df = df[df["Risk_Level"].str.title() == risk_level.title()]
    if project_type:
        df = df[df["Project_Type"].str.title() == project_type.title()]
    if project_phase:
        df = df[df["Project_Phase"].str.title() == project_phase.title()]
    if experience_level:
        df = df[df["Team_Experience_Level"].str.title() == experience_level.title()]

    return {"total": len(df), "data": df_to_json(df)}


@router.get("/by-type", summary="Distribuição de risco por tipo de projeto")
def get_risk_by_type(
    project_type: Optional[str] = Query(None, description="Filtrar por tipo de projeto"),
    risk_level: Optional[str]   = Query(None, description="Filtrar por nível de risco"),
):
    df = load_gold("risk_by_type.parquet")

    if project_type:
        df = df[df["Project_Type"].str.title() == project_type.title()]
    if risk_level:
        df = df[df["Risk_Level"].str.title() == risk_level.title()]

    return {"total": len(df), "data": df_to_json(df)}


@router.get("/by-methodology", summary="Risco por metodologia e experiência do time")
def get_risk_by_methodology(
    methodology: Optional[str]       = Query(None, description="Filtrar por metodologia (ex: Agile)"),
    experience_level: Optional[str]  = Query(None, description="Filtrar por experiência do time"),
):
    df = load_gold("risk_by_methodology.parquet")

    if methodology:
        df = df[df["Methodology_Used"].str.title() == methodology.title()]
    if experience_level:
        df = df[df["Team_Experience_Level"].str.title() == experience_level.title()]

    return {"total": len(df), "data": df_to_json(df)}


@router.get("/factors", summary="Resumo dos fatores de risco por nível")
def get_risk_factors(
    risk_level: Optional[str] = Query(None, description="Filtrar por nível de risco (ex: High)"),
):
    df = load_gold("risk_factors_summary.parquet")

    if risk_level:
        df = df[df["Risk_Level"].str.title() == risk_level.title()]

    return {"total": len(df), "data": df_to_json(df)}