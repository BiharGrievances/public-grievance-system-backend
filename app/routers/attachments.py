import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.attachment import Attachment
from app.models.complaint import Complaint

router = APIRouter(prefix="/attachments", tags=["Attachments"])

UPLOAD_DIR = "uploads"

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".pdf", ".mp4", ".mov", ".avi"
}

MAX_FILE_SIZE_MB = 5  # 5 MB limit


def validate_file(file: UploadFile):
    # 1️⃣ Check extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # 2️⃣ Check file size
    file.file.seek(0, os.SEEK_END)
    size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)

    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE_MB} MB")


@router.post("/upload")
def upload_attachment(
    complaint_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # 1️⃣ Check complaint exists
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # 2️⃣ Validate file
    validate_file(file)

    # 3️⃣ Create complaint-specific folder
    complaint_folder = os.path.join(UPLOAD_DIR, f"complaint_{complaint_id}")
    os.makedirs(complaint_folder, exist_ok=True)

    # 4️⃣ Safe file path
    safe_filename = file.filename.replace(" ", "_")
    file_path = os.path.join(complaint_folder, safe_filename)

    # 5️⃣ Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 6️⃣ Save metadata in DB
    attachment = Attachment(
        complaint_id=complaint_id,
        file_name=safe_filename,
        file_path=file_path,
        file_type=file.content_type
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return {
        "message": "Attachment uploaded successfully",
        "attachment_id": attachment.id,
        "file_name": attachment.file_name,
        "file_path": file_path
    }
