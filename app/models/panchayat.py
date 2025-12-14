from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Panchayat(Base):
    __tablename__ = "panchayats"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, nullable=False)
    block = Column(String, nullable=False)
    name = Column(String, nullable=False)

    # IMPORTANT: relationship only, no FK here
    complaints = relationship(
        "Complaint",
        back_populates="panchayat",
        passive_deletes=True
    )
