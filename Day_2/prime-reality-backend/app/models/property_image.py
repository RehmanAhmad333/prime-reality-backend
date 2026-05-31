# This module defines the PropertyImage model for the Prime Reality backend application. The PropertyImage model is used to store images associated with properties listed on the platform. It includes fields for the property ID (foreign key to the properties table), the image URL (stored in S3), whether the image is the primary image for the property, the display order of the image, and a timestamp for when the image was created. This allows for multiple images to be associated with each property and provides flexibility in how they are displayed on the frontend.

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func
from app.core.database import Base

class PropertyImage(Base):
    __tablename__ = "property_images"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String, nullable=False)   # S3 URL
    is_primary = Column(Boolean, default=False) # Indicates if this image is the primary image for the property, which can be used to determine which image to display first on the frontend. Only one image per property should have this set to True.
    display_order = Column(Integer, default=0)  # Index for ordering images for display
    created_at = Column(TIMESTAMP, server_default=func.now())