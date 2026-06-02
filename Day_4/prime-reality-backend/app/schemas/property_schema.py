from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PropertyImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class PropertyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    property_type: str  # apartment/villa/land/commercial
    price: float
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[int] = None
    location_lat: float   # from frontend map
    location_lng: float
    address: str
    city: str
    state: str
    zip_code: str
    tag: Optional[str] = None
    label: Optional[str] = None
    category: Optional[str] = None  # residential/commercial/industrial

class PropertyResponse(BaseModel):
    id: int
    seller_id: int
    title: str
    description: Optional[str]
    property_type: str
    price: float
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    area_sqft: Optional[int]
    address: str
    city: str
    state: str
    zip_code: str
    status: str
    featured: bool
    views_count: int
    tag: Optional[str]
    label: Optional[str]
    category: Optional[str]
    created_at: datetime
    images: List[PropertyImageBase] = []
    
    class Config:
        from_attributes = True

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    property_type: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None


