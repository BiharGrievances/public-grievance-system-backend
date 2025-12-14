from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.complaint_schema import ComplaintCreate, ComplaintResponse
from app.models.complaint import Complaint
from app.models.panchayat import Panchayat
from app.security.rate_limiter import rate_limit

router = APIRouter(prefix="/complaints", tags=["Complaints"])

@router.post("/", response_model=ComplaintResponse)
def create_complaint(
    request: Request,
    data: ComplaintCreate,
    db: Session = Depends(get_db)
):
    # Rate limit: 5 complaints / minute / IP
    ip = request.client.host
    rate_limit(f"complaint:{ip}", limit=5, window=60)

    if data.district_id != 37:
        raise HTTPException(status_code=400, detail="Only Vaishali supported")

    if data.panchayat_id == 0:
        if not data.panchayat_other_name:
            raise HTTPException(
                status_code=400,
                detail="Other Panchayat name required"
            )
        panchayat_id = None
    else:
        panchayat = db.query(Panchayat).filter(
            Panchayat.id == data.panchayat_id
        ).first()
        if not panchayat:
            raise HTTPException(status_code=404, detail="Invalid Panchayat ID")
        panchayat_id = panchayat.id

    complaint = Complaint(
        district_id=data.district_id,
        block=data.block,
        panchayat_id=panchayat_id,
        panchayat_other_name=data.panchayat_other_name,
        name=data.name,
        mobile=data.mobile,
        email=data.email,
        complaint_type=data.complaint_type,
        consent_to_share=data.consent_to_share,
        subject=data.subject[:200],
        description=data.description[:2000],
    )

    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return complaint
