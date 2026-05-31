# booking madule use for booking a property for a visit by a buyer. It will store the property id, buyer id, preferred date and time for the visit, status of the booking (pending, confirmed, cancelled) and any additional notes from the buyer. This will allow buyers to schedule visits to properties they are interested in and sellers/agents to manage those bookings effectively.   

from sqlalchemy import Column, Integer, TIMESTAMP, String, ForeignKey, func # Importing necessary SQLAlchemy components for defining the Booking model
from app.core.database import Base # Importing the Base class from the database module to create the Booking model as a SQLAlchemy model

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    preferred_date = Column(TIMESTAMP, nullable=False)
    status = Column(String(20), default="pending")  # pending, confirmed, cancelled
    notes = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())