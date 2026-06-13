import re
from fastapi import Request, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.rate_limit import limiter
from app.models.user import User
from app.models.property import Property
from app.models.chat_history import ChatHistory
from app.schemas.ai_schema import (
    ChatRequest, ChatResponse, PricePredictionResponse,
    RecommendationResponse, DescriptionRequest, DescriptionResponse,
    ImageClassifyResponse, VoiceSearchRequest, VoiceSearchResponse,
    VirtualTourRequest, VirtualTourResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["AI Features"])


# -------------------- 1. Chatbot --------------------
@router.post(
    "/chat/send",
    response_model=ChatResponse,
    summary="Send a message to AI chatbot",
    description="Stores user query in chat history and returns a mock reply. AI team will replace with actual LLM integration."
)
@limiter.limit("100/minute")
def chat_endpoint(
    request: Request,
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if payload.property_id:
            prop_exists = db.query(Property).filter(
                Property.id == payload.property_id
            ).first()

            if not prop_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Property with ID {payload.property_id} not found."
                )

        chat_entry = ChatHistory(
            user_id=current_user.id,
            property_id=payload.property_id,
            message=payload.message,
            reply=None,
            context_snapshot=None
        )

        db.add(chat_entry)
        db.commit()
        db.refresh(chat_entry)

        dummy_reply = (
            f"Thank you for your question: '{payload.message}'. "
            "Our AI assistant is currently learning. "
            "Please contact seller directly for immediate response."
        )

        chat_entry.reply = dummy_reply
        db.commit()

        return ChatResponse(
            reply=dummy_reply,
            context=[{"property_id": payload.property_id}] if payload.property_id else [],
            conversation_id=chat_entry.id
        )

    except HTTPException:
        raise
    except SQLAlchemyError as db_error:
        db.rollback()
        logger.error(f"Database error in chat_endpoint: {str(db_error)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while saving your message."
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat_endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected processing error occurred."
        )


# -------------------- 2. Price Prediction --------------------
@router.get(
    "/predict-price/{property_id}",
    response_model=PricePredictionResponse,
    summary="Get AI price prediction for a property",
    description="Returns a mock predicted price (±5‑10%) based on property's current price. Tazaeen will replace with ML model."
)
@limiter.limit("100/minute")
def predict_price(
    request: Request,
    property_id: int,
    db: Session = Depends(get_db)
):
    try:
        prop = db.query(Property).filter(Property.id == property_id).first()

        if not prop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found for price evaluation."
            )

        try:
            base_price = float(prop.price) if prop.price else 500000.0
        except (ValueError, TypeError):
            base_price = 500000.0

        predicted = base_price * 0.95 if base_price < 1000000 else base_price * 1.05

        return PricePredictionResponse(
            property_id=property_id,
            predicted_price=round(predicted, 2),
            confidence=0.87,
            estimated_price_range={
                "min": round(predicted * 0.9, 2),
                "max": round(predicted * 1.1, 2)
            }
        )

    except HTTPException:
        raise
    except SQLAlchemyError as db_error:
        logger.error(f"Database operation failed in predict_price: {str(db_error)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal system error accessing real estate data."
        )
    except Exception as e:
        logger.error(f"Unexpected processing fault in predict_price: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Execution processing breakdown on price model estimation."
        )


# -------------------- 3. Recommendations --------------------
@router.get(
    "/recommendations/{property_id}",
    response_model=RecommendationResponse,
    summary="Get similar property recommendations",
    description="Returns up to 5 properties with similar city or type. Mock similarity score 0.75. Tazaeen will replace with real recommendation engine."
)
@limiter.limit("100/minute")
def get_recommendations(
    request: Request,
    property_id: int,
    db: Session = Depends(get_db)
):
    try:
        prop = db.query(Property).filter(Property.id == property_id).first()

        if not prop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target reference property not found."
            )

        similar = db.query(Property).filter(
            Property.id != property_id,
            Property.status == "approved",
            (
                (Property.city == prop.city) |
                (Property.property_type == prop.property_type)
            )
        ).limit(5).all()

        recommended = []

        for p in similar:
            try:
                price_val = float(p.price) if p.price else 0.0
            except (ValueError, TypeError):
                price_val = 0.0

            recommended.append({
                "id": p.id,
                "title": p.title,
                "price": price_val,
                "city": p.city,
                "property_type": p.property_type,
                "similarity_score": 0.75
            })

        return RecommendationResponse(
            property_id=property_id,
            recommended_properties=recommended
        )

    except HTTPException:
        raise
    except SQLAlchemyError as db_error:
        logger.error(f"Database context error in get_recommendations: {str(db_error)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database failed to filter similar recommendations."
        )
    except Exception as e:
        logger.error(f"Error compiling recommendations list: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal application engine crash during recommendations generation."
        )


# -------------------- 4. Description Generator --------------------
@router.post(
    "/generate-description",
    response_model=DescriptionResponse,
    summary="Generate property description from features",
    description="Creates a mock property description based on input attributes. Hibba will replace with OpenAI call."
)
@limiter.limit("100/minute")
def generate_description(
    request: Request,
    req: DescriptionRequest
):
    try:
        if req.price <= 0 or req.area_sqft <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Price and Area dimensions metrics must be greater than zero."
            )

        mock_desc = f"""
Stunning {req.property_type} located in the heart of {req.city}.
This {req.bedrooms} bedroom, {req.bathrooms} bathroom property offers {req.area_sqft} sqft of living space.
Priced at ${req.price:,.2f}, this home features modern amenities and is close to schools, shopping, and parks.
Perfect for families or investors. Schedule your viewing today!
"""

        return DescriptionResponse(description=mock_desc.strip())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failure formatting static description parser: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed parsing description attributes data inputs."
        )


# -------------------- 5. Image Classification --------------------
@router.post(
    "/classify-image",
    response_model=ImageClassifyResponse,
    summary="Classify property type from image",
    description="Mock classification returning 'villa' with 92% confidence. Hibba will replace with ResNet/CNN model."
)
@limiter.limit("100/minute")
def classify_image(request: Request):
    try:
        return ImageClassifyResponse(
            property_type="villa",
            confidence=0.92,
            detected_objects=["swimming pool", "garden", "garage"]
        )
    except Exception as e:
        logger.error(f"Image structural analysis engine breakdown: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model analyzer processing interface pipeline error."
        )


# -------------------- 6. Voice Search --------------------
@router.post(
    "/voice-search",
    response_model=VoiceSearchResponse,
    summary="Convert voice/text to property filters",
    description="Parses natural language text and extracts property filters (type, price, bedrooms). Ifrah will enhance NLP."
)
@limiter.limit("100/minute")
def voice_search(
    request: Request,
    req: VoiceSearchRequest
):
    try:
        if not req.text or not req.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voice query script translation cannot be blank text string input."
            )

        text = req.text.lower()
        filters = {}

        if "villa" in text:
            filters["property_type"] = "villa"
        elif "apartment" in text:
            filters["property_type"] = "apartment"
        elif "land" in text:
            filters["property_type"] = "land"

        if "under" in text and "$" in text:
            match = re.search(r"\$?(\d+(?:\.\d+)?)\s*(k|million)?", text)
            if match:
                try:
                    num = float(match.group(1))
                    if match.group(2) == "k":
                        num *= 1000
                    elif match.group(2) == "million":
                        num *= 1000000
                    filters["price_max"] = num
                except (ValueError, IndexError):
                    pass

        if "bedroom" in text or "bedrooms" in text:
            match = re.search(r"(\d+)\s*bedroom", text)
            if match:
                try:
                    filters["bedrooms"] = int(match.group(1))
                except (ValueError, IndexError):
                    pass

        return VoiceSearchResponse(
            filters=filters,
            original_text=req.text
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Regular expression or algorithmic query string crash: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Natural processing script analyzer engine failure error."
        )


# -------------------- 7. Virtual Tour --------------------
@router.post(
    "/virtual-tour",
    response_model=VirtualTourResponse,
    summary="Generate textual walkthrough from images",
    description="Mock virtual tour description based on image URLs. Ifrah will replace with vision model (GPT-4V)."
)
@limiter.limit("100/minute")
def virtual_tour(
    request: Request,
    req: VirtualTourRequest
):
    try:
        walkthrough = """
As you enter the property, you are greeted by a spacious foyer with marble flooring.
To your left is a large living room with floor-to-ceiling windows offering panoramic views.
The kitchen features modern appliances and a central island.
Upstairs, you'll find three generously sized bedrooms and a master suite with walk-in closet.
The backyard includes a patio and landscaped garden.
"""
        return VirtualTourResponse(
            walkthrough_text=walkthrough.strip(),
            estimated_duration_minutes=3
        )
    except Exception as e:
        logger.error(f"Virtual rendering framework engine crash: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed rendering dynamic text generation stream."
        )