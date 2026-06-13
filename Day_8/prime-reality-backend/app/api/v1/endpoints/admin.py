from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.models.property import Property
from app.schemas.admin_schema import (
    PendingPropertyResponse,
    UserListResponse,
    MessageResponse,
    FeatureToggleResponse
)

from app.tasks.email_tasks import send_matching_alerts
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(require_role("admin"))])

@router.get("/properties/pending", response_model=list[PendingPropertyResponse])
def get_pending_properties(db: Session = Depends(get_db)):
    properties = db.query(Property).filter(Property.status == "pending").all()
    return properties

@router.put("/properties/{property_id}/approve", response_model=MessageResponse)
def approve_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    prop.status = "approved"
    db.commit()

    try:
        send_matching_alerts.delay(property_id)
        logger.info(f"Queued matching alerts for property ID {property_id}")
    except Exception as e:
        logger.error(f"Failed to queue matching alerts: {str(e)}")
    
    return {"message": "Property approved"}


@router.put("/properties/{property_id}/reject", response_model=MessageResponse)
def reject_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    prop.status = "rejected"
    db.commit()
    return {"message": "Property rejected"}

@router.put("/properties/{property_id}/feature", response_model=FeatureToggleResponse)
def toggle_featured(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    prop.featured = not prop.featured
    db.commit()
    return {"featured": prop.featured}

@router.get("/users", response_model=list[UserListResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# change user role (buyer, seller, admin) by admin only
@router.put("/users/{user_id}/role", response_model=MessageResponse)
def change_user_role(user_id: int, role: str, db: Session = Depends(get_db)):
    if role not in ["buyer", "seller", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be buyer, seller, or admin.")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role
    db.commit()
    return {"message": f"User role updated to {role}"}

# admin del any saller only 
@router.delete("/users/sellers/{user_id}", response_model=MessageResponse)
def delete_seller(user_id: int, db: Session = Depends(get_db)):
    seller = db.query(User).filter(User.id == user_id, User.role == "seller").first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    db.delete(seller)
    db.commit()
    return {"message": "Seller deleted successfully"}


# admin del any buyer only
@router.delete("/users/buyers/{user_id}", response_model=MessageResponse)   
def delete_buyer(user_id: int, db: Session = Depends(get_db)):
    buyer = db.query(User).filter(User.id == user_id, User.role == "buyer").first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    db.delete(buyer)
    db.commit()
    return {"message": "Buyer deleted successfully"}