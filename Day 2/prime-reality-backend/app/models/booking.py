from sqlalchemy import Column, Integer, TIMESTAMP, String, ForeignKey, func
from app.core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    preferred_date = Column(TIMESTAMP, nullable=False)
    status = Column(String(20), default="pending")  # pending, confirmed, cancelled
    notes = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())