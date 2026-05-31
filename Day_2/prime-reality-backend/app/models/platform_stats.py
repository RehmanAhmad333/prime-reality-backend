# This module defines the PlatformStat model for the Prime Reality backend application. The PlatformStat model is used to store various statistics about the platform, such as the total number of properties listed, total inquiries made, and total users registered. It includes fields for a unique stat key, the corresponding stat value, and a timestamp for when the statistic was last updated. This allows for tracking and analyzing key metrics about the platform's performance and user engagement over time.

from sqlalchemy import Column, Integer, String, BigInteger, TIMESTAMP, func
from app.core.database import Base

class PlatformStat(Base):
    __tablename__ = "platform_stats"

    id = Column(Integer, primary_key=True)
    stat_key = Column(String(100), unique=True, nullable=False)
    stat_value = Column(BigInteger, nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())