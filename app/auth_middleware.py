from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.database import get_db
from app.models.admin_user import AdminUser
from sqlalchemy.orm import Session


# ======================================
# CONFIG (FREE / LOCAL)
# ======================================
SECRET_KEY = "CHANGE_THIS_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ======================================
# SECURITY OBJECTS
# ======================================
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ======================================
# PASSWORD HELPERS
# ======================================
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ======================================
# TOKEN CREATION
# ======================================
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "iss": "DrAshutoshPublicGrievanceSystem",
        "type": "access"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ======================================
# ADMIN AUTH DEPENDENCY
# ======================================
def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> AdminUser:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username: Optional[str] = payload.get("sub")
        token_type = payload.get("type")

        if username is None or token_type != "access":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    admin = db.query(AdminUser).filter(
        AdminUser.username == username
    ).first()

    if admin is None:
        raise credentials_exception

    return admin
