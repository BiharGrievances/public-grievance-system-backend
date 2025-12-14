from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.district import District

router = APIRouter(prefix="/districts", tags=["Districts"])

@router.get("/")
def get_districts(db: Session = Depends(get_db)):
    return db.query(District).all()
