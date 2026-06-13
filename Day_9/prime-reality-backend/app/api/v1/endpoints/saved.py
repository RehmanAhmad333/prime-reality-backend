# This file contains API endpoints related to saved properties in the real estate platform. It allows users to save properties they are interested in, view their saved properties, and remove properties from their saved list. The endpoints are protected with authentication to ensure only authorized users can manage their saved properties. This feature enhances user experience by allowing them to easily access and manage properties they like.

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.property import Property
from app.models.saved_property import SavedProperty
from app.schemas.saved_schema import SavedPropertyResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/saved", tags=["Saved Properties"])


@router.post(
    "/{property_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    summary="Save a property to buyer's list",
    description="Adds a property to the current user's saved properties list. Cannot be duplicate."
)
def save_property(
    property_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Check if property exists
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Property with ID {property_id} not found."
            )
        
        # Check if already saved
        existing = db.query(SavedProperty).filter(
            SavedProperty.user_id == current_user.id,
            SavedProperty.property_id == property_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Property already saved."
            )
        
        # Save
        saved = SavedProperty(user_id=current_user.id, property_id=property_id)
        db.add(saved)
        db.commit()
        return {"message": "Property saved successfully"}

    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        db.rollback()
        logger.error(f"Database error while saving property {property_id} for user {current_user.id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save property due to a database error."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in save_property: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while saving the property."
        )


@router.get(
    "/",
    response_model=list[SavedPropertyResponse],
    summary="Get all saved properties for current user",
    description="Returns list of saved property IDs and metadata for the authenticated buyer."
)
def get_saved_properties(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        saved = db.query(SavedProperty).filter(
            SavedProperty.user_id == current_user.id
        ).order_by(SavedProperty.saved_at.desc()).all()
        return saved

    except SQLAlchemyError as db_err:
        logger.error(f"Database error fetching saved properties for user {current_user.id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve saved properties from the database."
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_saved_properties: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching saved properties."
        )


@router.delete(
    "/{property_id}",
    response_model=dict,
    summary="Remove a saved property",
    description="Deletes a property from the current user's saved list."
)
def remove_saved_property(
    property_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        saved = db.query(SavedProperty).filter(
            SavedProperty.user_id == current_user.id,
            SavedProperty.property_id == property_id
        ).first()
        if not saved:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Saved property not found."
            )
        db.delete(saved)
        db.commit()
        return {"message": "Property removed from saved"}

    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        db.rollback()
        logger.error(f"Database error removing saved property {property_id} for user {current_user.id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove saved property due to a database error."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in remove_saved_property: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while removing the saved property."
        )