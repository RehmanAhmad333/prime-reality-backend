from pydantic import BaseModel
from datetime import datetime

class SavedPropertyResponse(BaseModel):
    id: int
    property_id: int
    saved_at: datetime
    
    class Config:
        from_attributes = True