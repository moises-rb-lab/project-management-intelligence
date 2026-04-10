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

router = APIRouter(prefix="/management", tags=["Management"])


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
@router.get("/projects", summary="Lista todos os projetos com KPIs")
def get_projects(
    status:     Optional[str] = Query(None, description="Filtrar por status (ex: Completed)"),
    region:     Optional[str] = Query(None, description="Filtrar por região (ex: North)"),
    department: Optional[str] = Query(None, description="Filtrar por departamento"),
    complexity: Optional[str] = Query(None, description="Filtrar por complexidade (ex: High)"),
):
    filters = {
        "status":     status,
        "region":     region,
        "department": department,
        "complexity": complexity,
    }
    data = fetch("vw_mgmt_projects_kpis", filters)
    return {"total": len(data), "data": data}


@router.get("/status", summary="Resumo de projetos por status")
def get_status_summary():
    data = fetch("vw_mgmt_status_summary")
    return {"total": len(data), "data": data}


@router.get("/department-region", summary="Custo e benefício por departamento e região")
def get_department_region(
    department: Optional[str] = Query(None, description="Filtrar por departamento"),
    region:     Optional[str] = Query(None, description="Filtrar por região"),
):
    filters = {
        "department": department,
        "region":     region,
    }
    data = fetch("vw_mgmt_department_region", filters)
    return {"total": len(data), "data": data}


@router.get("/phase-complexity", summary="Distribuição por fase e complexidade")
def get_phase_complexity(
    phase:      Optional[str] = Query(None, description="Filtrar por fase"),
    complexity: Optional[str] = Query(None, description="Filtrar por complexidade"),
):
    filters = {
        "phase":      phase,
        "complexity": complexity,
    }
    data = fetch("vw_mgmt_phase_complexity", filters)
    return {"total": len(data), "data": data}