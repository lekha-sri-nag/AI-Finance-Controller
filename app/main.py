from fastapi import FastAPI

from app.api.routes import router
from app.api.investigation_routes import router as investigation_router
from app.api.decision_routes import router as decision_router

from app.database.database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Finance Controller",
    description="AI-powered financial control and invoice investigation system",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Finance Controller API is running",
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(router)
app.include_router(investigation_router)
app.include_router(decision_router)
