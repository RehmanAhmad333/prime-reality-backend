from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from app.core.database import Base

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    search_query = Column(String, nullable=False)   # e.g., "3 bedroom villa under 500k"
    filters_used = Column(String)                   # JSON string of applied filters
    results_count = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())