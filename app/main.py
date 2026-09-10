import os
from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI

from app.auth.user_routes import router as user_router
from app.api.routes import router
from app.api.investigation_routes import router as investigation_router
from app.api.decision_routes import router as decision_router
from app.api.ingestion_routes import router as ingestion_router
from app.auth.routes import router as auth_router
from app.api.document_ingestion_routes import router as document_ingestion_router
from app.api.dynamic_processing_routes import router as dynamic_processing_router

from app.database.database import Base, engine, SessionLocal
from app.database.models import User
from app.auth.security import hash_password

Base.metadata.create_all(bind=engine)
def create_initial_admin():
    username = os.getenv("INITIAL_ADMIN_USERNAME")
    password = os.getenv("INITIAL_ADMIN_PASSWORD")

    if not username or not password:
        return

    db = SessionLocal()

    try:
        existing_user = db.query(User).first()

        if existing_user:
            return

        admin = User(
            username=username,
            password_hash=hash_password(password),
            role="admin",
            is_active=True
        )

        db.add(admin)
        db.commit()

    finally:
        db.close()


create_initial_admin()


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
app.include_router(ingestion_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(document_ingestion_router)
app.include_router(dynamic_processing_router)
