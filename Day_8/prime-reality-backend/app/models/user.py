# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    role = Column(String(50), default="buyer")  # buyer, seller, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # --- SELLER CASCADE ---
    properties = relationship(
        "Property", 
        back_populates="seller", 
        cascade="all, delete-orphan"
    )

    # --- BUYER CASCADE 
    saved_properties = relationship(
        "SavedProperty", 
        back_populates="buyer", 
        cascade="all, delete-orphan",
        primaryjoin="User.id==SavedProperty.user_id"
    )

    # --- INQUIRY CASCADE ---
    inquiries = relationship(
        "Inquiry", 
        back_populates="buyer", 
        cascade="all, delete-orphan"
    )
