# This file contains API endpoints related to inquiries in the real estate platform. It allows buyers to create inquiries for properties, view their inquiries, and allows sellers to manage inquiries for their properties. Admins can also update inquiry statuses. The endpoints are protected with authentication and role-based access control to ensure only authorized users can perform certain actions.

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.property import Property
from app.models.inquiry import Inquiry
from app.schemas.inquiry_schema import InquiryCreate, InquiryResponse
from app.tasks.email_tasks import send_inquiry_email

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])


@router.post(
    "/",
    response_model=InquiryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send an inquiry about a property",
    description="Allows a buyer to send a message to the seller. The inquiry is saved with status 'pending' and an email notification is sent to the seller asynchronously via Celery."
)
def create_inquiry(
    inquiry: InquiryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Verify property exists
        property_obj = db.query(Property).filter(Property.id == inquiry.property_id).first()
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Property with ID {inquiry.property_id} not found."
            )
        
        # Create the inquiry record
        new_inquiry = Inquiry(
            property_id=inquiry.property_id,
            buyer_id=current_user.id,
            message=inquiry.message,
            status="pending"
        )
        db.add(new_inquiry)
        db.commit()
        db.refresh(new_inquiry)
        
        # Send email asynchronously to the seller
        seller = db.query(User).filter(User.id == property_obj.seller_id).first()
        if seller and seller.email:
            try:
                send_inquiry_email.delay(
                    seller.email,
                    current_user.full_name,
                    property_obj.title,
                    inquiry.message
                )
                logger.info(f"Inquiry email queued for seller {seller.email} (property {property_obj.id})")
            except Exception as email_err:
                # Log but do not fail the inquiry creation if email fails
                logger.error(f"Failed to queue inquiry email: {str(email_err)}")
        
        return new_inquiry

    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        db.rollback()
        logger.error(f"Database error while creating inquiry for user {current_user.id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send inquiry due to a database error."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in create_inquiry: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your inquiry."
        )


@router.get(
    "/",
    response_model=list[InquiryResponse],
    summary="Get all inquiries for current user",
    description="Buyers see their own sent inquiries. Sellers see all inquiries received on their properties. Admin sees all inquiries."
)
def get_my_inquiries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if current_user.role == "seller":
            # Get all properties owned by this seller
            properties = db.query(Property).filter(Property.seller_id == current_user.id).all()
            property_ids = [p.id for p in properties]
            if property_ids:
                inquiries = db.query(Inquiry).filter(Inquiry.property_id.in_(property_ids)).order_by(Inquiry.created_at.desc()).all()
            else:
                inquiries = []
        elif current_user.role == "admin":
            # Admin can see all inquiries
            inquiries = db.query(Inquiry).order_by(Inquiry.created_at.desc()).all()
        else:
            # Buyer: see only inquiries they created
            inquiries = db.query(Inquiry).filter(Inquiry.buyer_id == current_user.id).order_by(Inquiry.created_at.desc()).all()
        return inquiries

    except SQLAlchemyError as db_err:
        logger.error(f"Database error while fetching inquiries for user {current_user.id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve inquiries from the database."
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_my_inquiries: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching inquiries."
        )