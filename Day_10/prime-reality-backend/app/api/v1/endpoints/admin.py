from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.models.property import Property
from app.models.booking import Booking
from app.models.inquiry import Inquiry
from app.schemas.admin_schema import (
    PendingPropertyResponse,
    UserListResponse,
    MessageResponse,
    FeatureToggleResponse
)
from app.tasks.email_tasks import send_matching_alerts
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_role("admin"))]
)

# ==================== Property Management ====================

@router.get(
    "/properties/pending",
    response_model=list[PendingPropertyResponse],
    summary="Get all pending properties",
    description="Returns a list of all properties with status 'pending'. Only accessible by admin."
)
def get_pending_properties(db: Session = Depends(get_db)):
    try:
        properties = db.query(Property).filter(Property.status == "pending").all()
        return properties
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_pending_properties: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch pending properties from database."
        )


@router.put(
    "/properties/{property_id}/approve",
    response_model=MessageResponse,
    summary="Approve a pending property",
    description="Changes property status from 'pending' to 'approved' and triggers email alerts to matching users."
)
def approve_property(property_id: int, db: Session = Depends(get_db)):
    try:
        prop = db.query(Property).filter(Property.id == property_id).first()
        if not prop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Property with ID {property_id} not found."
            )
        
        prop.status = "approved"
        db.commit()

        # Trigger email alerts for matching user alerts
        try:
            send_matching_alerts.delay(property_id)
            logger.info(f"Queued matching alerts for property ID {property_id}")
        except Exception as e:
            # Log but don't fail the approval if Celery/Redis is down
            logger.error(f"Failed to queue matching alerts for property {property_id}: {str(e)}")

        return {"message": "Property approved"}

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in approve_property: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update property status due to database error."
        )


@router.put(
    "/properties/{property_id}/reject",
    response_model=MessageResponse,
    summary="Reject a pending property",
    description="Changes property status from 'pending' to 'rejected'."
)
def reject_property(property_id: int, db: Session = Depends(get_db)):
    try:
        prop = db.query(Property).filter(Property.id == property_id).first()
        if not prop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Property with ID {property_id} not found."
            )
        
        prop.status = "rejected"
        db.commit()
        return {"message": "Property rejected"}

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in reject_property: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reject property due to database error."
        )


@router.put(
    "/properties/{property_id}/feature",
    response_model=FeatureToggleResponse,
    summary="Toggle featured status of a property",
    description="Marks or unmarks a property as featured. Only visible on frontend after approval."
)
def toggle_featured(property_id: int, db: Session = Depends(get_db)):
    try:
        prop = db.query(Property).filter(Property.id == property_id).first()
        if not prop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Property with ID {property_id} not found."
            )
        
        prop.featured = not prop.featured
        db.commit()
        return {"featured": prop.featured}

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in toggle_featured: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to toggle featured status."
        )


# ==================== User Management ====================

@router.get(
    "/users",
    response_model=list[UserListResponse],
    summary="Get all users",
    description="Returns a list of all registered users (buyers, sellers, admins)."
)
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_all_users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users from database."
        )


@router.put(
    "/users/{user_id}/role",
    response_model=MessageResponse,
    summary="Change a user's role",
    description="Update role of any user to 'buyer', 'seller', or 'admin'."
)
def change_user_role(user_id: int, role: str, db: Session = Depends(get_db)):
    try:
        if role not in ["buyer", "seller", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role. Must be 'buyer', 'seller', or 'admin'."
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found."
            )
        
        user.role = role
        db.commit()
        return {"message": f"User role updated to {role}"}

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in change_user_role: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user role due to database error."
        )


@router.delete(
    "/users/sellers/{user_id}",
    response_model=MessageResponse,
    summary="Delete a seller",
    description="Removes a seller account permanently. Only sellers can be deleted; buyer or admin accounts are not affected."
)
def delete_seller(user_id: int, db: Session = Depends(get_db)):
    try:
        seller = db.query(User).filter(User.id == user_id, User.role == "seller").first()
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found or user is not a seller."
            )
        
        db.delete(seller)
        db.commit()
        return {"message": "Seller deleted successfully"}

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in delete_seller: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete seller due to database error."
        )


@router.delete(
    "/users/buyers/{user_id}",
    response_model=MessageResponse,
    summary="Delete a buyer",
    description="Removes a buyer account permanently. Only buyers can be deleted."
)
def delete_buyer(user_id: int, db: Session = Depends(get_db)):
    try:
        buyer = db.query(User).filter(User.id == user_id, User.role == "buyer").first()
        if not buyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Buyer not found or user is not a buyer."
            )
        
        db.delete(buyer)
        db.commit()
        return {"message": "Buyer deleted successfully"}

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in delete_buyer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete buyer due to database error."
        )

# This endpoint provides aggregated statistics for the admin dashboard, including total counts of users, properties (broken down by status), bookings, and inquiries. It allows admins to quickly assess the overall activity and health of the platform. The endpoint handles potential database errors gracefully, ensuring that any issues are logged and appropriate error messages are returned in the API response.
@router.get(
    "/dashboard/stats",
    response_model=dict,
    summary="Get admin dashboard statistics",
    description="Returns aggregated counts: users, properties (by status), bookings, inquiries."
)
def get_admin_stats(db: Session = Depends(get_db)):
    try:
        total_users = db.query(User).count()
        total_properties = db.query(Property).count()
        pending_properties = db.query(Property).filter(Property.status == "pending").count()
        approved_properties = db.query(Property).filter(Property.status == "approved").count()
        rejected_properties = db.query(Property).filter(Property.status == "rejected").count()
        total_bookings = db.query(Booking).count()
        total_inquiries = db.query(Inquiry).count()
        
        return {
            "total_users": total_users,
            "total_properties": total_properties,
            "pending_properties": pending_properties,
            "approved_properties": approved_properties,
            "rejected_properties": rejected_properties,
            "total_bookings": total_bookings,
            "total_inquiries": total_inquiries
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_admin_stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard statistics."
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_admin_stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )