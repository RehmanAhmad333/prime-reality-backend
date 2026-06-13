# This file contains API endpoints related to bookings in the real estate platform. It allows buyers to create bookings for properties, view their bookings, and allows sellers to manage bookings for their properties. Admins can also update booking statuses. The endpoints are protected with authentication and role-based access control to ensure only authorized users can perform certain actions.
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.property import Property
from app.models.booking import Booking
from app.schemas.booking_schema import BookingCreate, BookingResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Schedule a property viewing",
    description="Allows a buyer to request a viewing for a specific property. The booking status is initially set to 'pending'."
)
def create_booking(
    booking: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Verify property exists
        property_obj = db.query(Property).filter(Property.id == booking.property_id).first()
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Property with ID {booking.property_id} not found."
            )
        
        new_booking = Booking(
            property_id=booking.property_id,
            buyer_id=current_user.id,
            preferred_date=booking.preferred_date,
            notes=booking.notes,
            status="pending"
        )
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking

    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        db.rollback()
        logger.error(f"Database error while creating booking for user {current_user.id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to schedule viewing due to a database error."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in create_booking: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while scheduling the viewing."
        )


@router.get(
    "/",
    response_model=list[BookingResponse],
    summary="Get all bookings for current user",
    description="If the user is a buyer, returns their own booking requests. If seller, returns bookings on their properties. Admin sees all bookings."
)
def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if current_user.role == "seller":
            properties = db.query(Property).filter(Property.seller_id == current_user.id).all()
            property_ids = [p.id for p in properties]
            if property_ids:
                bookings = db.query(Booking).filter(Booking.property_id.in_(property_ids)).all()
            else:
                bookings = []
        elif current_user.role == "admin":
            # Admin can see all bookings
            bookings = db.query(Booking).all()
        else:
            # Buyer
            bookings = db.query(Booking).filter(Booking.buyer_id == current_user.id).all()
        return bookings

    except SQLAlchemyError as db_err:
        logger.error(f"Database error fetching bookings for user {current_user.id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve bookings from the database."
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_my_bookings: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching bookings."
        )


@router.put(
    "/{booking_id}/status",
    response_model=dict,
    summary="Update booking status (confirm/cancel)",
    description="Allows a seller or admin to change the booking status to 'confirmed' or 'cancelled'."
)
def update_booking_status(
    booking_id: int,
    status: str,  # confirmed, cancelled
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if status not in ["confirmed", "cancelled"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be either 'confirmed' or 'cancelled'."
            )

        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Booking with ID {booking_id} not found."
            )
        
        # Check permission: only seller of the property or admin
        property_obj = db.query(Property).filter(Property.id == booking.property_id).first()
        if property_obj.seller_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this booking."
            )
        
        booking.status = status
        db.commit()
        return {"message": f"Booking {status}"}

    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        db.rollback()
        logger.error(f"Database error updating booking {booking_id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update booking status due to a database error."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in update_booking_status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating booking status."
        )