# This file contains API endpoints related to platform statistics in the real estate platform. It provides an endpoint to retrieve various platform metrics such as total network users, visit multiplier, rural listings, total properties, and total users. The endpoint aggregates data from both dynamic counts (like total properties and users) and static stats stored in the platform_stats table. This allows the frontend to display up-to-date platform statistics to users and admins.

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db
from app.models.platform_stats import PlatformStat
from app.models.user import User
from app.models.property import Property
from app.schemas.platform_schema import PlatformStatsResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/platform", tags=["Platform"])


@router.get(
    "/stats",
    response_model=PlatformStatsResponse,
    summary="Get platform statistics",
    description="Returns dynamic and static platform metrics including total properties, total users, network usage stats (12M+), visit multiplier (12X), and rural listings (1M+)."
)
def get_platform_stats(db: Session = Depends(get_db)):
    try:
        # Get dynamic counts
        total_properties = db.query(Property).filter(Property.status == "approved").count()
        total_users = db.query(User).count()

        # Get static stats from platform_stats table with fallback defaults
        stats_dict = {
            "total_network_users": 0,
            "visit_multiplier": 0,
            "rural_listings": 0
        }

        try:
            stats = db.query(PlatformStat).all()
            for s in stats:
                stats_dict[s.stat_key] = s.stat_value
        except SQLAlchemyError as e:
            # Log but continue with defaults
            logger.warning(f"Could not fetch platform_stats from database: {str(e)}")

        # Update dynamic values (override any static values with real-time counts)
        stats_dict["total_properties"] = total_properties
        stats_dict["total_users"] = total_users

        return PlatformStatsResponse(
            total_network_users=stats_dict["total_network_users"],
            visit_multiplier=stats_dict["visit_multiplier"],
            rural_listings=stats_dict["rural_listings"],
            total_properties=total_properties,
            total_users=total_users
        )

    except SQLAlchemyError as db_err:
        logger.error(f"Database error while fetching platform stats: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve platform statistics due to a database error."
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_platform_stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching platform statistics."
        )