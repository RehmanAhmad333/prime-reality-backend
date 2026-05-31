# This module defines the User model for the Prime Reality backend application. The User model is used to store information about users of the platform, including their email, password hash, full name, phone number, role (buyer, seller, admin), whether their account is active, and a timestamp for when the account was created. This model serves as the core representation of a user in the application and is essential for managing user authentication, authorization, and profile information.

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
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