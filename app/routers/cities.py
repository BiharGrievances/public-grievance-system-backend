from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.city import City

router = APIRouter(prefix="/cities", tags=["Cities"])

@router.get("/")
def get_cities(district_id: int, db: Session = Depends(get_db)):
    return db.query(City).filter(City.district_id == district_id).all()
