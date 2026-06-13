# This file contains API endpoints related to saved properties in the real estate platform. It allows users to save properties they are interested in, view their saved properties, and remove properties from their saved list. The endpoints are protected with authentication to ensure only authorized users can manage their saved properties. This feature enhances user experience by allowing them to easily access and manage properties they like.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.property import Property
from app.models.saved_property import SavedProperty
from app.schemas.saved_schema import SavedPropertyResponse

router = APIRouter(prefix="/saved", tags=["Saved Properties"])

@router.post("/{property_id}", status_code=201)
def save_property(
    property_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if property exists
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Check if already saved
    existing = db.query(SavedProperty).filter(
        SavedProperty.user_id == current_user.id,
        SavedProperty.property_id == property_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Property already saved")
    
    # Save
    saved = SavedProperty(user_id=current_user.id, property_id=property_id)
    db.add(saved)
    db.commit()
    return {"message": "Property saved successfully"}

@router.get("/", response_model=list[SavedPropertyResponse])
def get_saved_properties(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    saved = db.query(SavedProperty).filter(SavedProperty.user_id == current_user.id).all()
    return saved

@router.delete("/{property_id}")
def remove_saved_property(
    property_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    saved = db.query(SavedProperty).filter(
        SavedProperty.user_id == current_user.id,
        SavedProperty.property_id == property_id
    ).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved property not found")
    db.delete(saved)
    db.commit()
    return {"message": "Property removed from saved"}