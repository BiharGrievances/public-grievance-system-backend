from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.panchayat import Panchayat

router = APIRouter(prefix="/panchayats", tags=["Panchayats"])

@router.get("/")
def get_panchayats(
    district_id: int,
    block: str = None,
    db: Session = Depends(get_db)
):
    """
    Returns all panchayats for a given district.
    Optional filter: block name.
    Always appends an 'Other' option.
    """

    # Base query
    query = db.query(Panchayat).filter(Panchayat.district_id == district_id)

    # If block filter is used
    if block:
        query = query.filter(Panchayat.block == block)

    panchayats = query.all()

    results = [
        {
            "id": p.id,
            "district_id": p.district_id,
            "block": p.block,
            "name": p.name
        }
        for p in panchayats
    ]

    # Add universal "Other" option
    results.append({
        "id": 0,
        "district_id": district_id,
        "block": block if block else "Other",
        "name": "Other"
    })

    return results
