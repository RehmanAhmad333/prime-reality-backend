# This file defines the Booking model for the real estate platform. The Booking model represents a booking made by a buyer for a property. It includes fields such as property_id, buyer_id, preferred_date, status, notes, and created_at. The model uses SQLAlchemy for database interactions and includes relationships to the Property and User models through foreign keys. This allows us to easily query related data when working with bookings in the application.

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