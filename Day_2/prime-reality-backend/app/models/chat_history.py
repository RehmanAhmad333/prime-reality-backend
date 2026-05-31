# This module defines the ChatHistory model for the Prime Reality backend application. The ChatHistory model is used to store the history of interactions between users and the AI assistant regarding specific properties. It includes fields for the user ID, property ID, user message, AI reply, a snapshot of the property context at the time of the interaction, and a timestamp for when the interaction occurred. This allows for tracking and analyzing user interactions with the AI assistant over time.

from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func, String
from app.core.database import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for each chat history entry
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL")) # Foreign key to the users table, allowing for tracking which user had the interaction. If the user is deleted, this field will be set to NULL.
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="SET NULL")) # Foreign key to the properties table, allowing for tracking which property the interaction was about. If the property is deleted, this field will be set to NULL.  
    message = Column(Text, nullable=False) 
    reply = Column(Text)
    context_snapshot = Column(String)  # JSON string of property context
    created_at = Column(TIMESTAMP, server_default=func.now())