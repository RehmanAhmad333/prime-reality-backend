from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, String
from app.core.database import Base

class PropertyView(Base):
    __tablename__ = "property_views"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # null if anonymous
    ip_address = Column(String(45))
    viewed_at = Column(TIMESTAMP, server_default=func.now())