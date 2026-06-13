from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmailAlertCreate(BaseModel):
    city: Optional[str] = None
    property_type: Optional[str] = None  # villa, apartment, land, commercial
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    bedrooms: Optional[int] = None
    frequency: str = "weekly"  # daily or weekly

class EmailAlertResponse(BaseModel):
    id: int
    filters_json: str
    is_active: bool
    frequency: str
    last_sent_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class AlertResponse(BaseModel):
    message: str
    alert_id: int