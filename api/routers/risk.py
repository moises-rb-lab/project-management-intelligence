import os
from fastapi import APIRouter, HTTPException, Query
from dotenv import load_dotenv
from supabase import create_client
from typing import Optional

# ─────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────
load_dotenv()

client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

router = APIRouter(prefix="/risk", tags=["Risk"])


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def fetch(view: str, filters: dict = {}) -> list:
    try:
        query = client.table(view).select("*")
        for column, value in filters.items():
            if value is not None:
                query = query.ilike(column, value)
        response = query.execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────
@router.get("/profile", summary="Perfil de risco por projeto")
def get_risk_profile(
    risk_level:       Optional[str] = Query(None, description="Filtrar por nível de risco (ex: High)"),
    project_type:     Optional[str] = Query(None, description="Filtrar por tipo de projeto (ex: It)"),
    project_phase:    Optional[str] = Query(None, description="Filtrar por fase (ex: Planning)"),
    experience_level: Optional[str] = Query(None, description="Filtrar por experiência do time (ex: Senior)"),
):
    filters = {
        "risk_level":           risk_level,
        "project_type":         project_type,
        "project_phase":        project_phase,
        "team_experience_level": experience_level,
    }
    data = fetch("vw_risk_profile", filters)
    return {"total": len(data), "data": data}


@router.get("/by-type", summary="Distribuição de risco por tipo de projeto")
def get_risk_by_type(
    project_type: Optional[str] = Query(None, description="Filtrar por tipo de projeto"),
    risk_level:   Optional[str] = Query(None, description="Filtrar por nível de risco"),
):
    filters = {
        "project_type": project_type,
        "risk_level":   risk_level,
    }
    data = fetch("vw_risk_by_type", filters)
    return {"total": len(data), "data": data}


@router.get("/by-methodology", summary="Risco por metodologia e experiência do time")
def get_risk_by_methodology(
    methodology:      Optional[str] = Query(None, description="Filtrar por metodologia (ex: Agile)"),
    experience_level: Optional[str] = Query(None, description="Filtrar por experiência do time"),
):
    filters = {
        "methodology_used":      methodology,
        "team_experience_level": experience_level,
    }
    data = fetch("vw_risk_by_methodology", filters)
    return {"total": len(data), "data": data}


@router.get("/factors", summary="Resumo dos fatores de risco por nível")
def get_risk_factors(
    risk_level: Optional[str] = Query(None, description="Filtrar por nível de risco (ex: High)"),
):
    filters = {
        "risk_level": risk_level,
    }
    data = fetch("vw_risk_factors_summary", filters)
    return {"total": len(data), "data": data}