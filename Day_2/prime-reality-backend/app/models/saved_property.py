from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from app.core.database import Base

class SavedProperty(Base):
    __tablename__ = "saved_properties"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    saved_at = Column(TIMESTAMP, server_default=func.now())