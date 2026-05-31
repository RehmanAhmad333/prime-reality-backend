# This module defines the Review model for the Prime Reality backend application. The Review model is used to store reviews and testimonials from users about properties listed on the platform. It includes fields for the property ID (foreign key to the properties table), reviewer name, reviewer role (e.g., buyer, seller, agent), reviewer image (stored in S3), a short quote or highlight from the review, the full review text, a rating (1-5), whether the review is featured, display order for sorting featured reviews, and a timestamp for when the review was created. This allows for collecting and displaying user feedback on properties, which can help build trust and provide insights for potential buyers and sellers.

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
    display_order = Column(Integer, default=0)  # Index for ordering reviews for display
    created_at = Column(TIMESTAMP, server_default=func.now())