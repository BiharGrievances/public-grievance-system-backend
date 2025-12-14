from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.models.admin_user import AdminUser
from app.auth_middleware import (
    create_access_token,
    verify_password,
    hash_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# ===============================
# ADMIN LOGIN
# ===============================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(AdminUser)
        .filter(AdminUser.username == form_data.username)
        .first()
    )

    if not user or not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ===============================
# ONE-TIME ADMIN BOOTSTRAP
# ===============================
@router.post("/bootstrap-admin")
def bootstrap_admin(db: Session = Depends(get_db)):
    """
    Creates first admin.
    DISABLED automatically in production.
    """

    # 🔒 HARD BLOCK IN PRODUCTION
    if os.getenv("ENV") == "production":
        raise HTTPException(
            status_code=403,
            detail="Bootstrap disabled in production"
        )

    existing_admin = db.query(AdminUser).first()
    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin already exists"
        )

    admin = AdminUser(
        username="Ashu",
        password_hash=hash_password("Ashu")
    )

    db.add(admin)
    db.commit()

    return {
        "message": "Admin created"
    }
