# This file contains API endpoints related to reviews in the real estate platform. It provides an endpoint to retrieve featured reviews that are marked as featured in the database. The reviews are ordered by their display order and limited to a maximum of 5 reviews. This allows the frontend to display a curated list of featured reviews on the platform, enhancing user trust and engagement. The endpoint is protected with authentication to ensure only authorized users can access the reviews.

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db
from app.models.review import Review
from app.schemas.review_schema import ReviewResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get(
    "/featured",
    response_model=list[ReviewResponse],
    summary="Get featured reviews (testimonials)",
    description="Returns up to 5 reviews marked as featured, ordered by display_order (ascending). Used for homepage testimonials carousel."
)
def get_featured_reviews(db: Session = Depends(get_db)):
    try:
        reviews = db.query(Review).filter(
            Review.is_featured == True
        ).order_by(
            Review.display_order
        ).limit(5).all()
        return reviews

    except SQLAlchemyError as db_err:
        logger.error(f"Database error while fetching featured reviews: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve featured reviews due to a database error."
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_featured_reviews: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching featured reviews."
        )