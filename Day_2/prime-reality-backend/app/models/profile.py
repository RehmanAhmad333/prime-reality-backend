# This module defines the Profile model for the Prime Reality backend application. The Profile model is used to store additional information about users, such as their avatar URL, bio, preferred location, budget range, and notification preferences. It includes a foreign key to the users table to link each profile to a specific user, and timestamps for when the profile was created and last updated. This allows for a more personalized experience for users on the platform and enables features like targeted notifications and personalized property recommendations.

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, func
from app.core.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False) # Foreign key to the users table, ensuring that each profile is linked to a specific user. If the user is deleted, the profile will also be deleted (CASCADE). The unique constraint ensures that each user can only have one profile. 
    avatar_url = Column(String)   # S3 URL for the user's avatar image, allowing users to personalize their profile with a picture. This field is optional and can be null if the user has not uploaded an avatar.
    bio = Column(Text)
    preferred_location = Column(String(255))  # User's preferred location for property searches
    budget_min = Column(Integer)
    budget_max = Column(Integer)
    notification_preferences = Column(String)  # JSON string 
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())