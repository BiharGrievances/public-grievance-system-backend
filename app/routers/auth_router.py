from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.admin_user import AdminUser
from app.auth_middleware import create_access_token, verify_password
from app.security.rate_limiter import rate_limit

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    rate_limit(request)

    user = db.query(AdminUser)\
        .filter(AdminUser.username == form_data.username)\
        .first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@router.post("/bootstrap-admin")
def bootstrap_admin(db: Session = Depends(get_db)):
    from app.models.admin_user import AdminUser
    from app.auth_middleware import hash_password

    admin = db.query(AdminUser).first()
    if admin:
        return {"message": "Admin already exists"}

    admin = AdminUser(
        username="Ashu",
        password_hash=hash_password("Ashu")
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return {"message": "Admin created"}
