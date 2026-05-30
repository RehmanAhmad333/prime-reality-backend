from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey, func, SmallInteger
from app.core.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="SET NULL"))
    reviewer_name = Column(String(255), nullable=False)
    reviewer_role = Column(String(255))
    reviewer_image = Column(String)   # S3 URL
    quote = Column(Text)              # short highlight
    review_text = Column(Text, nullable=False)
    rating = Column(SmallInteger)     # 1-5
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())