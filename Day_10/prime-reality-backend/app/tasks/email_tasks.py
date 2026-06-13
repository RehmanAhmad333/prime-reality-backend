# app/tasks/email_tasks.py

import json
import logging
from datetime import datetime, timedelta

import sendgrid
from sendgrid.helpers.mail import Mail
from celery.schedules import crontab
from sqlalchemy.exc import SQLAlchemyError

from .celery_app import celery_app
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.email_alert import EmailAlert
from app.models.property import Property
from app.models.user import User
from app.services.email_service import send_email_sync


logger = logging.getLogger(__name__)


# Celery Beat Schedule – Daily and Weekly Email Alerts
celery_app.conf.beat_schedule = {
    "weekly-property-alerts": {
        "task": "app.tasks.email_tasks.send_weekly_alerts",
        "schedule": crontab(day_of_week="monday", hour=9, minute=0),
    },
    "daily-property-alerts": {
        "task": "app.tasks.email_tasks.send_daily_alerts",
        "schedule": crontab(hour=9, minute=0),
    },
}

celery_app.conf.timezone = "UTC"


# -------------------- 1. Send Inquiry Email --------------------
@celery_app.task
def send_inquiry_email(
    seller_email: str,
    buyer_name: str,
    property_title: str,
    message: str
):
    """
    Send inquiry email to seller when buyer asks about a property.
    """

    try:
        if not seller_email:
            return {"error": "Seller email is required."}

        if not settings.SENDGRID_API_KEY:
            return {"error": "SendGrid API key is missing."}

        if not settings.SENDGRID_FROM_EMAIL:
            return {"error": "SendGrid sender email is missing."}

        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

        email_body = f"""
New inquiry for your property: {property_title}

From: {buyer_name}

Message:
{message}

Please login to your dashboard to reply.
"""

        mail = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=seller_email,
            subject=f"New Inquiry: {property_title}",
            plain_text_content=email_body.strip()
        )

        response = sg.send(mail)

        logger.info(
            f"Inquiry email sent to {seller_email}. "
            f"Status Code: {response.status_code}"
        )

        return {
            "status": response.status_code,
            "message": "Email sent successfully."
        }

    except Exception as e:
        logger.error(f"Error sending inquiry email: {str(e)}")
        return {"error": str(e)}


# -------------------- 2. Send Matching Alerts --------------------
@celery_app.task
def send_matching_alerts(property_id: int):
    """
    Send alerts to users when a new approved property matches their saved criteria.
    """

    db = SessionLocal()

    try:
        new_property = db.query(Property).filter(
            Property.id == property_id
        ).first()

        if not new_property:
            logger.warning(f"Property with ID {property_id} not found.")
            return {"message": "Property not found."}

        if new_property.status != "approved":
            logger.info(
                f"Property {property_id} is not approved. Alert skipped."
            )
            return {"message": "Property is not approved."}

        alerts = db.query(EmailAlert).filter(
            EmailAlert.is_active == True
        ).all()

        sent_count = 0

        for alert in alerts:
            try:
                filters = json.loads(alert.filters_json or "{}")
            except json.JSONDecodeError:
                logger.warning(
                    f"Invalid filters_json for alert ID {alert.id}"
                )
                continue

            matches = True

            property_price = float(new_property.price or 0)

            if filters.get("city"):
                if not new_property.city or filters["city"].lower() != new_property.city.lower():
                    matches = False

            if filters.get("property_type"):
                if filters["property_type"] != new_property.property_type:
                    matches = False

            if filters.get("price_min"):
                if property_price < float(filters["price_min"]):
                    matches = False

            if filters.get("price_max"):
                if property_price > float(filters["price_max"]):
                    matches = False

            if filters.get("bedrooms"):
                if new_property.bedrooms != int(filters["bedrooms"]):
                    matches = False

            if not matches:
                continue

            user = db.query(User).filter(
                User.id == alert.user_id
            ).first()

            if not user or not user.email:
                continue

            subject = f"New Property Matching Your Search: {new_property.title}"

            content = f"""
A new property matching your criteria has been listed!

Title: {new_property.title}
Price: ${property_price:,.2f}
Location: {new_property.city}
Type: {new_property.property_type}
Bedrooms: {new_property.bedrooms}

View full details: {settings.FRONTEND_URL}/properties/{new_property.id}
"""

            send_email_sync(user.email, subject, content.strip())

            sent_count += 1

            logger.info(
                f"Alert email sent to {user.email} "
                f"for property {new_property.id}"
            )

        return {
            "message": "Matching alerts processed successfully.",
            "emails_sent": sent_count
        }

    except SQLAlchemyError as db_error:
        db.rollback()
        logger.error(f"Database error in send_matching_alerts: {str(db_error)}")
        return {"error": "Database error occurred while sending matching alerts."}

    except Exception as e:
        logger.error(f"Unexpected error in send_matching_alerts: {str(e)}")
        return {"error": str(e)}

    finally:
        db.close()


# -------------------- 3. Send Weekly Alerts --------------------
@celery_app.task
def send_weekly_alerts():
    """
    Send weekly digest of new properties to users with weekly email alerts.
    """

    db = SessionLocal()

    try:
        alerts = db.query(EmailAlert).filter(
            EmailAlert.is_active == True,
            EmailAlert.frequency == "weekly"
        ).all()

        sent_count = 0
        one_week_ago = datetime.utcnow() - timedelta(days=7)

        for alert in alerts:
            try:
                filters = json.loads(alert.filters_json or "{}")
            except json.JSONDecodeError:
                logger.warning(
                    f"Invalid filters_json for weekly alert ID {alert.id}"
                )
                continue

            user = db.query(User).filter(
                User.id == alert.user_id
            ).first()

            if not user or not user.email:
                continue

            query = db.query(Property).filter(
                Property.status == "approved",
                Property.created_at >= one_week_ago
            )

            query = apply_property_filters(query, filters)

            new_properties = query.all()

            if not new_properties:
                continue

            subject = "Weekly Property Alert – New Listings Matching Your Search"

            content = f"Hi {user.full_name},\n\n"
            content += f"We found {len(new_properties)} new properties matching your preferences:\n\n"

            for prop in new_properties:
                price = float(prop.price or 0)
                content += f"- {prop.title}: ${price:,.2f} in {prop.city}\n"

            content += f"\nView all: {settings.FRONTEND_URL}/properties"

            send_email_sync(user.email, subject, content)

            alert.last_sent_at = datetime.utcnow()
            sent_count += 1

        db.commit()

        logger.info(f"Weekly alerts sent successfully. Total: {sent_count}")

        return {
            "message": "Weekly alerts sent successfully.",
            "emails_sent": sent_count
        }

    except SQLAlchemyError as db_error:
        db.rollback()
        logger.error(f"Database error in send_weekly_alerts: {str(db_error)}")
        return {"error": "Database error occurred while sending weekly alerts."}

    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in send_weekly_alerts: {str(e)}")
        return {"error": str(e)}

    finally:
        db.close()


# -------------------- 4. Send Daily Alerts --------------------
@celery_app.task
def send_daily_alerts():
    """
    Send daily digest of new properties to users with daily email alerts.
    """

    db = SessionLocal()

    try:
        alerts = db.query(EmailAlert).filter(
            EmailAlert.is_active == True,
            EmailAlert.frequency == "daily"
        ).all()

        sent_count = 0
        one_day_ago = datetime.utcnow() - timedelta(days=1)

        for alert in alerts:
            try:
                filters = json.loads(alert.filters_json or "{}")
            except json.JSONDecodeError:
                logger.warning(
                    f"Invalid filters_json for daily alert ID {alert.id}"
                )
                continue

            user = db.query(User).filter(
                User.id == alert.user_id
            ).first()

            if not user or not user.email:
                continue

            query = db.query(Property).filter(
                Property.status == "approved",
                Property.created_at >= one_day_ago
            )

            query = apply_property_filters(query, filters)

            new_properties = query.all()

            if not new_properties:
                continue

            subject = "Daily Property Alert – New Listings Matching Your Search"

            content = f"Hi {user.full_name},\n\n"
            content += f"We found {len(new_properties)} new properties matching your preferences:\n\n"

            for prop in new_properties:
                price = float(prop.price or 0)
                content += f"- {prop.title}: ${price:,.2f} in {prop.city}\n"

            content += f"\nView all: {settings.FRONTEND_URL}/properties"

            send_email_sync(user.email, subject, content)

            alert.last_sent_at = datetime.utcnow()
            sent_count += 1

        db.commit()

        logger.info(f"Daily alerts sent successfully. Total: {sent_count}")

        return {
            "message": "Daily alerts sent successfully.",
            "emails_sent": sent_count
        }

    except SQLAlchemyError as db_error:
        db.rollback()
        logger.error(f"Database error in send_daily_alerts: {str(db_error)}")
        return {"error": "Database error occurred while sending daily alerts."}

    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in send_daily_alerts: {str(e)}")
        return {"error": str(e)}

    finally:
        db.close()


# -------------------- Helper Function --------------------
def apply_property_filters(query, filters: dict):
    """
    Apply saved alert filters to property query.
    """

    if filters.get("city"):
        query = query.filter(
            Property.city.ilike(f"%{filters['city']}%")
        )

    if filters.get("property_type"):
        query = query.filter(
            Property.property_type == filters["property_type"]
        )

    if filters.get("price_min"):
        query = query.filter(
            Property.price >= float(filters["price_min"])
        )

    if filters.get("price_max"):
        query = query.filter(
            Property.price <= float(filters["price_max"])
        )

    if filters.get("bedrooms"):
        query = query.filter(
            Property.bedrooms == int(filters["bedrooms"])
        )

    return query