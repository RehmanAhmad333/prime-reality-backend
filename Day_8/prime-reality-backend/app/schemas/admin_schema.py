# app/schemas/admin_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PendingPropertyResponse(BaseModel):
    id: int
    title: str
    property_type: str
    price: float
    city: str
    status: str
    seller_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str

class FeatureToggleResponse(BaseModel):
    featured: bool