from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.complaint import Complaint
from app.auth_middleware import get_current_admin
from app.security.rate_limiter import rate_limit_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_admin)]
)

# ===============================
# ADMIN DASHBOARD SUMMARY
# ===============================
@router.get("/summary")
def complaint_summary(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Admin dashboard summary:
    Count complaints by status
    """

    rate_limit_admin(request)

    total = db.query(func.count(Complaint.id)).scalar()

    submitted = db.query(func.count(Complaint.id))\
        .filter(Complaint.status == "submitted").scalar()

    under_review = db.query(func.count(Complaint.id))\
        .filter(Complaint.status == "under_review").scalar()

    resolved = db.query(func.count(Complaint.id))\
        .filter(Complaint.status == "resolved").scalar()

    rejected = db.query(func.count(Complaint.id))\
        .filter(Complaint.status == "rejected").scalar()

    return {
        "total": total,
        "submitted": submitted,
        "under_review": under_review,
        "resolved": resolved,
        "rejected": rejected
    }


# ===============================
# GET ALL / FILTERED COMPLAINTS
# ===============================
@router.get("/complaints")
def get_complaints(
    request: Request,
    status: str | None = Query(default=None),
    block: str | None = Query(default=None),
    district_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    """
    Admin: Fetch complaints with optional filters
    """

    rate_limit_admin(request)

    query = db.query(Complaint)

    if status:
        query = query.filter(Complaint.status == status)

    if block:
        query = query.filter(Complaint.block == block)

    if district_id:
        query = query.filter(Complaint.district_id == district_id)

    return query.order_by(Complaint.id.desc()).all()


# ===============================
# UPDATE COMPLAINT STATUS
# ===============================
@router.put("/complaints/{complaint_id}/status")
def update_complaint_status(
    complaint_id: int,
    status: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Admin: Update complaint status
    """

    rate_limit_admin(request)

    allowed_statuses = {
        "submitted",
        "under_review",
        "resolved",
        "rejected"
    }

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed: {allowed_statuses}"
        )

    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    complaint.status = status
    db.commit()

    return {
        "complaint_id": complaint_id,
        "new_status": status
    }
