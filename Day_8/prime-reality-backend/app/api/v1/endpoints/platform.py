# This file contains API endpoints related to platform statistics in the real estate platform. It provides an endpoint to retrieve various platform metrics such as total network users, visit multiplier, rural listings, total properties, and total users. The endpoint aggregates data from both dynamic counts (like total properties and users) and static stats stored in the platform_stats table. This allows the frontend to display up-to-date platform statistics to users and admins.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.platform_stats import PlatformStat
from app.models.user import User
from app.models.property import Property
from app.schemas.platform_schema import PlatformStatsResponse

router = APIRouter(prefix="/platform", tags=["Platform"])

@router.get("/stats", response_model=PlatformStatsResponse)
def get_platform_stats(db: Session = Depends(get_db)):
    # Get dynamic counts
    total_properties = db.query(Property).filter(Property.status == "approved").count()
    total_users = db.query(User).count()
    
    # Get static stats from platform_stats table
    stats_dict = {}
    stats = db.query(PlatformStat).all()
    for s in stats:
        stats_dict[s.stat_key] = s.stat_value
    
    # Update dynamic values
    stats_dict["total_properties"] = total_properties
    stats_dict["total_users"] = total_users
    
    return PlatformStatsResponse(
        total_network_users=stats_dict.get("total_network_users", 0),
        visit_multiplier=stats_dict.get("visit_multiplier", 0),
        rural_listings=stats_dict.get("rural_listings", 0),
        total_properties=total_properties,
        total_users=total_users
    )