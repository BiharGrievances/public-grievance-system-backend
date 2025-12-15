from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.models.admin_user import AdminUser
from app.auth_middleware import (
    create_access_token,
    verify_password,
    hash_password
)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])


# -------------------------------
# LOGIN
# -------------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    admin = db.query(AdminUser).filter(
        AdminUser.username == form_data.username
    ).first()

    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": admin.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# -------------------------------
# BOOTSTRAP ADMIN (SAFE)
# -------------------------------
@router.post("/bootstrap-admin")
def bootstrap_admin(db: Session = Depends(get_db)):
    env = os.getenv("ENV", "development")

    if env == "production":
        raise HTTPException(
            status_code=403,
            detail="Bootstrap disabled in production"
        )

    existing = db.query(AdminUser).first()
    if existing:
        return {"message": "Admin already exists"}

    admin = AdminUser(
        username="Ashu",
        password_hash=hash_password("Ashu")
    )

    db.add(admin)
    db.commit()

    return {"message": "Admin created"}
