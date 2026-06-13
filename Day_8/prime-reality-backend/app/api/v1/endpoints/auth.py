# This module defines the authentication endpoints for the Prime Reality backend application. It includes routes for user registration and login. The registration endpoint allows new users to create an account by providing their email, password, full name, phone number, and role. The login endpoint allows existing users to authenticate by providing their email and password. Both endpoints return JWT access and refresh tokens upon successful authentication. The module uses SQLAlchemy for database interactions and relies on the security utilities defined in the app's core security module for password hashing and token generation.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["Authentication"]) # Yeh router authentication se related endpoints ko group karta hai. Iska prefix "/auth" hai, matlab ke is router ke sare endpoints "/auth" se start honge, jaise ke "/auth/register" aur "/auth/login". Tags "Authentication" se API documentation me in endpoints ko categorize kiya jayega, taki developers ko samajhne me asani ho ke ye endpoints user authentication ke liye hain.

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        phone=user_data.phone,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate tokens
    access_token = create_access_token(data={"sub": new_user.email, "role": new_user.role})
    refresh_token = create_refresh_token(data={"sub": new_user.email})
    
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Account disabled")
    
    # Generate tokens
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {"access_token": access_token, "refresh_token": refresh_token}