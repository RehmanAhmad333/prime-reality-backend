# This file contains API endpoints related to bookings in the real estate platform. It allows buyers to create bookings for properties, view their bookings, and allows sellers to manage bookings for their properties. Admins can also update booking statuses. The endpoints are protected with authentication and role-based access control to ensure only authorized users can perform certain actions.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.property import Property
from app.models.booking import Booking
from app.schemas.booking_schema import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", status_code=201)
def create_booking(
    booking: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    property = db.query(Property).filter(Property.id == booking.property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    
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

@router.get("/", response_model=list[BookingResponse])
def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "seller":
        properties = db.query(Property).filter(Property.seller_id == current_user.id).all()
        property_ids = [p.id for p in properties]
        bookings = db.query(Booking).filter(Booking.property_id.in_(property_ids)).all()
    else:
        bookings = db.query(Booking).filter(Booking.buyer_id == current_user.id).all()
    return bookings

@router.put("/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    status: str,  # confirmed, cancelled
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Check permission: only seller or admin
    property = db.query(Property).filter(Property.id == booking.property_id).first()
    if property.seller_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    booking.status = status
    db.commit()
    return {"message": f"Booking {status}"}