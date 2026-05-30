from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func
from app.core.database import Base

class EmailAlert(Base):
    __tablename__ = "email_alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filters_json = Column(String, nullable=False)  # e.g., {"price_min": 500000, "city": "Beverly Hills", "property_type": "villa"}
    is_active = Column(Boolean, default=True)
    frequency = Column(String(20), default="daily")  # daily, weekly
    last_sent_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())