from pydantic import BaseModel, Field
from typing import Optional

class ComplaintCreate(BaseModel):
    district_id: int = Field(..., description="Selected district ID")
    block: str = Field(..., description="Selected block name")
    panchayat_id: Optional[int] = Field(None, description="Selected panchayat ID (0 = Other)")
    panchayat_other_name: Optional[str] = Field(
        None, min_length=3, max_length=100,
        description="User-entered panchayat name if 'Other' is selected"
    )

    # User identity fields
    name: str = Field(..., min_length=3, max_length=100)
    mobile: str = Field(..., min_length=10, max_length=15)
    email: Optional[str] = Field(None)

    # Complaint type
    complaint_type: str = Field(
        ..., description="normal or confidential"
    )

    consent_to_share: bool = Field(
        ..., description="Should the complaint be shared with authorities?"
    )

    # Complaint content
    subject: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)


class ComplaintResponse(BaseModel):
    id: int
    district_id: int
    block: str
    panchayat_id: Optional[int]
    panchayat_other_name: Optional[str]
    name: str
    mobile: str
    email: Optional[str]
    complaint_type: str
    consent_to_share: bool
    subject: str
    description: str

    class Config:
        from_attributes = True
