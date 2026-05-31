# This module defines the SearchHistory model for the Prime Reality backend application. The SearchHistory model is used to store information about users' search queries and the filters they applied when searching for properties on the platform. It includes fields for the user ID (foreign key to the users table), the search query text, a JSON string of the filters used, the count of results returned for that search, and a timestamp for when the search was performed. This allows for tracking user search behavior and can be useful for analytics and improving search functionality in the future.

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