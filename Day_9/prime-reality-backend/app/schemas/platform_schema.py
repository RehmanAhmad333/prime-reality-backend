from pydantic import BaseModel
from typing import Dict, Any

class PlatformStatsResponse(BaseModel):
    total_network_users: int
    visit_multiplier: int
    rural_listings: int
    total_properties: int
    total_users: int
    # additional dynamic keys can be added as needed

    class Config:
        from_attributes = True