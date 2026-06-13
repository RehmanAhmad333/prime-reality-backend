# app/models/saved_property.py

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class SavedProperty(Base):
    __tablename__ = "saved_properties"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    saved_at = Column(TIMESTAMP, server_default=func.now())
     
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    buyer = relationship("User", back_populates="saved_properties", foreign_keys=[user_id])