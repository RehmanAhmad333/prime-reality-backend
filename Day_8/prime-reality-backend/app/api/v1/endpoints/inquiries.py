# This file contains API endpoints related to inquiries in the real estate platform. It allows buyers to create inquiries for properties, view their inquiries, and allows sellers to manage inquiries for their properties. Admins can also update inquiry statuses. The endpoints are protected with authentication and role-based access control to ensure only authorized users can perform certain actions.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.property import Property
from app.models.inquiry import Inquiry
from app.schemas.inquiry_schema import InquiryCreate, InquiryResponse
from app.tasks.email_tasks import send_inquiry_email

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])

@router.post("/", status_code=201)
def create_inquiry(
    inquiry: InquiryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    property = db.query(Property).filter(Property.id == inquiry.property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    new_inquiry = Inquiry(
        property_id=inquiry.property_id,
        buyer_id=current_user.id,
        message=inquiry.message,
        status="pending"
    )
    db.add(new_inquiry)
    db.commit()
    db.refresh(new_inquiry)
    
    # Send email asynchronously
    seller = db.query(User).filter(User.id == property.seller_id).first()
    if seller and seller.email:
        send_inquiry_email.delay(seller.email, current_user.full_name, property.title, inquiry.message)
    
    return new_inquiry

@router.get("/", response_model=list[InquiryResponse])
def get_my_inquiries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # For sellers: return inquiries on their properties
    if current_user.role == "seller":
        properties = db.query(Property).filter(Property.seller_id == current_user.id).all()
        property_ids = [p.id for p in properties]
        inquiries = db.query(Inquiry).filter(Inquiry.property_id.in_(property_ids)).all()
    else:
        inquiries = db.query(Inquiry).filter(Inquiry.buyer_id == current_user.id).all()
    return inquiries