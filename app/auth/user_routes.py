from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.auth.security import hash_password
from app.database.database import get_db
from app.database.models import User


router = APIRouter(
    prefix="/users",
    tags=["User Management"]
)


ALLOWED_ROLES = {
    "admin",
    "finance_controller",
    "finance_reviewer",
    "auditor"
}


class UserCreateRequest(BaseModel):
    username: str
    password: str
    role: str


@router.post("/")
def create_user(
    request: UserCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    username = request.username.strip()
    role = request.role.strip().lower()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty"
        )

    if len(request.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 8 characters"
        )

    if role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Allowed roles: {sorted(ALLOWED_ROLES)}"
        )

    existing_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    user_id = f"USR-{int(datetime.now(timezone.utc).timestamp() * 1000)}"

    new_user = User(
        user_id=user_id,
        username=username,
        password_hash=hash_password(request.password),
        role=role,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user": {
            "user_id": new_user.user_id,
            "username": new_user.username,
            "role": new_user.role,
            "is_active": new_user.is_active
        }
    }


@router.get("/")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin"))
):
    users = db.query(User).all()

    return [
        {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
            "is_active": user.is_active
        }
        for user in users
    ]