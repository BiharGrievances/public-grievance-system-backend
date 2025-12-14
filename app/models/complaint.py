from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    district_id = Column(Integer, nullable=False)
    block = Column(String, nullable=False)

    panchayat_id = Column(
        Integer,
        ForeignKey("panchayats.id", ondelete="SET NULL"),
        nullable=True
    )

    panchayat_other_name = Column(String, nullable=True)

    name = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    email = Column(String, nullable=True)

    complaint_type = Column(String, nullable=False)
    consent_to_share = Column(Boolean, default=True)

    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    status = Column(String, default="submitted")

    # 🔗 Relationships
    panchayat = relationship(
        "Panchayat",
        back_populates="complaints"
    )

    attachments = relationship(
        "Attachment",
        back_populates="complaint",
        cascade="all, delete-orphan"
    )
