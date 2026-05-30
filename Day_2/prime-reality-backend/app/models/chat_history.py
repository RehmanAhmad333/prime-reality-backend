from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func, String
from app.core.database import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="SET NULL"))
    message = Column(Text, nullable=False)
    reply = Column(Text)
    context_snapshot = Column(String)  # JSON string of property context
    created_at = Column(TIMESTAMP, server_default=func.now())