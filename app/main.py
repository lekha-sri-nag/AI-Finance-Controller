from fastapi import FastAPI
from app.api.routes import router

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