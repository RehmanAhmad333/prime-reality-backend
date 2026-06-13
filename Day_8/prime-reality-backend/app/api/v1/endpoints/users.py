# This module defines the user-related endpoints for the Prime Reality backend application. It includes routes for retrieving the current user's profile and updating the user's profile information. The `get_me` endpoint returns the authenticated user's details, while the `update_me` endpoint allows the user to update their full name and phone number. Both endpoints require authentication and use the `get_current_user` dependency to ensure that only authenticated users can access or modify their profile information. The module interacts with the database using SQLAlchemy sessions and commits changes when updating the user's profile.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me")
def update_me(full_name: str = None, phone: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if full_name:
        current_user.full_name = full_name
    if phone:
        current_user.phone = phone
    db.commit()
    return {"message": "Profile updated successfully"}