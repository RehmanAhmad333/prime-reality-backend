from pydantic import BaseModel
from datetime import datetime

class InquiryCreate(BaseModel):
    property_id: int
    message: str

class InquiryResponse(BaseModel):
    id: int
    property_id: int
    buyer_id: int
    message: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True