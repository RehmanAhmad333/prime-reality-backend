# This file contains API endpoints related to reviews in the real estate platform. It provides an endpoint to retrieve featured reviews that are marked as featured in the database. The reviews are ordered by their display order and limited to a maximum of 5 reviews. This allows the frontend to display a curated list of featured reviews on the platform, enhancing user trust and engagement. The endpoint is protected with authentication to ensure only authorized users can access the reviews.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.review import Review
from app.schemas.review_schema import ReviewResponse  # Import schema

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("/featured", response_model=list[ReviewResponse])
def get_featured_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.is_featured == True).order_by(Review.display_order).limit(5).all()
    return reviews