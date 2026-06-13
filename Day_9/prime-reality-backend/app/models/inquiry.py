# app/models/inquiry.py

from sqlalchemy import Column, Integer, Text, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship  # <--- IMPORTED FOR RELATIONSHIP
from app.core.database import Base

class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    
    # Added ondelete="CASCADE" for database level safety  
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    message = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, replied, closed
    created_at = Column(TIMESTAMP, server_default=func.now())

    #  FIXED: Added the missing relationship that SQLAlchemy was searching for 
    buyer = relationship("User", back_populates="inquiries")
