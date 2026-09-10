from sqlalchemy import Column, String, DateTime, Text, Boolean
import uuid
from datetime import datetime

from app.database.database import Base


class DecisionRecord(Base):
    __tablename__ = "decisions"

    decision_id = Column(String, primary_key=True)
    invoice_id = Column(String, nullable=False)
    recommendation_id = Column(String, nullable=False)
    decision = Column(String, nullable=False)
    decided_by = Column(String, nullable=False)
    decided_at = Column(DateTime, nullable=False)
    comments = Column(Text, default="")


class AuditRecord(Base):
    __tablename__ = "audit_records"

    audit_id = Column(String, primary_key=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    performed_by = Column(String, nullable=False)
    performed_at = Column(DateTime, nullable=False)
    details = Column(Text, nullable=False)


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )