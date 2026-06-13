from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Chatbot
class ChatRequest(BaseModel):
    message: str
    property_id: Optional[int] = None

class ChatResponse(BaseModel):
    reply: str
    context: Optional[List[Dict[str, Any]]] = None
    conversation_id: Optional[int] = None

# Price Prediction
class PricePredictionResponse(BaseModel):
    property_id: int
    predicted_price: float
    confidence: float
    estimated_price_range: Dict[str, float]  # e.g., {"min": 450000, "max": 550000}

# Recommendations
class RecommendationResponse(BaseModel):
    property_id: int
    recommended_properties: List[Dict[str, Any]]  # list of property objects

# Description Generator
class DescriptionRequest(BaseModel):
    property_type: str
    bedrooms: int
    bathrooms: int
    area_sqft: int
    city: str
    price: float
    amenities: Optional[List[str]] = None

class DescriptionResponse(BaseModel):
    description: str

# Image Classification
class ImageClassifyResponse(BaseModel):
    property_type: str  # apartment, villa, land, commercial
    confidence: float
    detected_objects: Optional[List[str]] = None

# Voice Search
class VoiceSearchRequest(BaseModel):
    text: str  # speech-to-text output

class VoiceSearchResponse(BaseModel):
    filters: Dict[str, Any]  # e.g., {"property_type": "villa", "bedrooms": 3, "price_max": 500000}
    original_text: str

# Virtual Tour
class VirtualTourRequest(BaseModel):
    image_urls: List[str]

class VirtualTourResponse(BaseModel):
    walkthrough_text: str
    estimated_duration_minutes: int