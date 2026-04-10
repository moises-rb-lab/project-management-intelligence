from fastapi import FastAPI
from api.routers import management_old, risk_old

app = FastAPI(
    title="Project Analytics API",
    description="API de analytics para gestão de projetos — arquitetura medalhão",
    version="1.0.0"
)

app.include_router(management_old.router)
app.include_router(risk_old.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Project Analytics API online"}