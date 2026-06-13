from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewResponse(BaseModel):
    id: int
    property_id: Optional[int]
    reviewer_name: str
    reviewer_role: Optional[str]
    reviewer_image: Optional[str]
    quote: Optional[str]
    review_text: str
    rating: int
    is_featured: bool
    display_order: int
    created_at: datetime

    class Config:
        from_attributes = True