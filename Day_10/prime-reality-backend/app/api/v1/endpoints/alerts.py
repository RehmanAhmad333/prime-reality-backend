import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.email_alert import EmailAlert
from app.schemas.alert_schema import EmailAlertCreate, EmailAlertResponse, AlertResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alerts", tags=["Email Alerts"])


@router.post(
    "/",
    response_model=AlertResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new email alert",
    description="Allows a buyer to set up daily or weekly property alerts based on filters like city, property type, price range, and bedrooms."
)
def create_alert(
    alert_data: EmailAlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new email alert for the current user safely."""
    try:
        filters = {
            "city": alert_data.city,
            "property_type": alert_data.property_type,
            "price_min": alert_data.price_min,
            "price_max": alert_data.price_max,
            "bedrooms": alert_data.bedrooms,
            "frequency": alert_data.frequency
        }
        # Remove None values cleanly
        filters = {k: v for k, v in filters.items() if v is not None}
        
        try:
            filters_string = json.dumps(filters)
        except (TypeError, ValueError) as json_err:
            logger.error(f"JSON serialization failed for alert filters: {str(json_err)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Provided filter criteria contains invalid data types."
            )
        
        new_alert = EmailAlert(
            user_id=current_user.id,
            filters_json=filters_string,
            frequency=alert_data.frequency,
            is_active=True
        )
        
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        
        return {"message": "Email alert created successfully", "alert_id": new_alert.id}

    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        db.rollback()
        logger.error(f"Database error during alert creation for user {current_user.id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save email alert due to a database exception."
        )
    except Exception as e:
        logger.error(f"Unexpected fault in create_alert: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected processing error occurred."
        )


@router.get(
    "/",
    response_model=list[EmailAlertResponse],
    summary="Get all active alerts for current user",
    description="Retrieves all email alerts that the authenticated user has created and are currently active."
)
def get_my_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        alerts = db.query(EmailAlert).filter(
            EmailAlert.user_id == current_user.id,
            EmailAlert.is_active == True
        ).all()
        return alerts

    except SQLAlchemyError as db_err:
        logger.error(f"Database fetch failed for user alerts {current_user.id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve alerts from the database."
        )
    except Exception as e:
        logger.error(f"Unexpected fault in get_my_alerts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while compiling your alerts list."
        )


@router.put(
    "/{alert_id}/toggle",
    response_model=dict,
    summary="Toggle alert active/inactive",
    description="Activate or deactivate an existing email alert without deleting it. Returns the new active state."
)
def toggle_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        alert = db.query(EmailAlert).filter(
            EmailAlert.id == alert_id,
            EmailAlert.user_id == current_user.id
        ).first()
        
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requested email alert not found or unauthorized access."
            )
        
        alert.is_active = not alert.is_active
        db.commit()
        return {"active": alert.is_active}

    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        db.rollback()
        logger.error(f"Database error toggling alert ID {alert_id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update alert configuration state."
        )
    except Exception as e:
        logger.error(f"Unexpected failure in toggle_alert: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Processing breakdown while updating alert status."
        )


@router.delete(
    "/{alert_id}",
    response_model=dict,
    summary="Delete an email alert",
    description="Permanently removes the specified email alert for the current user."
)
def delete_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        alert = db.query(EmailAlert).filter(
            EmailAlert.id == alert_id,
            EmailAlert.user_id == current_user.id
        ).first()
        
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert target does not exist or unauthorized access."
            )
        
        db.delete(alert)
        db.commit()
        return {"message": "Alert deleted"}

    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        db.rollback()
        logger.error(f"Database session execution failure during delete of alert {alert_id}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database failed to process the alert deletion requested."
        )
    except Exception as e:
        logger.error(f"Unexpected crash in delete_alert: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal application breakdown handling delete process flow."
        )