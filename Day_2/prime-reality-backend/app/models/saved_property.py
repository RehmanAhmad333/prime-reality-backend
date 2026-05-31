# This module defines the SavedProperty model for the Prime Reality backend application. The SavedProperty model is used to store information about properties that users have saved or bookmarked for later viewing. It includes fields for the user ID (foreign key to the users table), property ID (foreign key to the properties table), and a timestamp for when the property was saved. This allows users to easily access and manage their saved properties within the application.

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from app.core.database import Base

class SavedProperty(Base):
    __tablename__ = "saved_properties"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    saved_at = Column(TIMESTAMP, server_default=func.now()) 