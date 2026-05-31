# This module defines the PropertyView model for the Prime Reality backend application. The PropertyView model is used to track views of properties by users or anonymous visitors. It includes fields for the property ID (foreign key to the properties table), user ID (foreign key to the users table, nullable for anonymous views), IP address of the viewer, and a timestamp for when the view occurred. This allows for analytics on property views, such as tracking how many times a property has been viewed and by whom, which can be useful for sellers and agents to gauge interest in their listings.

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, String
from app.core.database import Base

class PropertyView(Base):
    __tablename__ = "property_views"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # null if anonymous
    ip_address = Column(String(45))  # IP address of the viewer
    viewed_at = Column(TIMESTAMP, server_default=func.now())