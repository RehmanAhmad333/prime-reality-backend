from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    property_id: int
    preferred_date: datetime
    notes: str = None

class BookingResponse(BaseModel):
    id: int
    property_id: int
    buyer_id: int
    preferred_date: datetime
    status: str
    notes: str = None
    created_at: datetime
    
    class Config:
        from_attributes = True