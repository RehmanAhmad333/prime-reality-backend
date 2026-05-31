# This module defines the Inquiry model for the Prime Reality backend application. The Inquiry model is used to store inquiries made by buyers about specific properties. It includes fields for the property ID, buyer ID, message content, status of the inquiry (pending, replied, closed), and a timestamp for when the inquiry was created. This allows buyers to communicate their interest in properties and sellers/agents to manage those inquiries effectively.

from sqlalchemy import Column, Integer, Text, String, ForeignKey, TIMESTAMP, func
from app.core.database import Base

class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, replied, closed
    created_at = Column(TIMESTAMP, server_default=func.now())