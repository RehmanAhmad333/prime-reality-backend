# This module defines the authentication endpoints for the Prime Reality backend application.
# It includes routes for user registration and login. Both endpoints return JWT access and
# refresh tokens upon successful authentication. The module uses SQLAlchemy for database
# interactions and relies on the security utilities defined in the app's core security module
# for password hashing and token generation.


#  prime-reality-backend/app/api/v1/endpoints/auth.py

import logging
from fastapi import APIRouter, Request, Depends, HTTPException, status
from jose import JWTError
import jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, Token, RefreshTokenRequest
from app.core.config import Settings
from app.core.rate_limit import limiter
from app.core.redis import redis_client
from app.core.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])
settings = Settings()


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="""
    Create a new user account.
    - **email**: Must be unique and valid email format
    - **password**: Minimum 6 characters
    - **role**: Optional, defaults to 'buyer'. Can be 'buyer', 'seller', or 'admin'
    - Returns access_token and refresh_token
    """,
    response_description="JWT tokens for authentication"
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if user exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
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
    
    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        db.rollback()
        logger.error(f"Database error during registration for email {user_data.email}: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating user account."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user and get tokens",
    description="""
    Login with email and password.
    - Returns access_token (expires in 30 minutes) and refresh_token (expires in 7 days)
    - Use the access_token in Authorization header as 'Bearer <token>' for protected endpoints
    """,
    response_description="JWT access and refresh tokens"
)
@limiter.limit("200/minute")   # this requires a request parameter
def login(request: Request, user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account disabled")
        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        refresh_token = create_refresh_token(data={"sub": user.email})
        return {"access_token": access_token, "refresh_token": refresh_token}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal error")

# This endpoint allows users to refresh their access token using a valid refresh token. It verifies the refresh token, checks if the user exists, and then generates a new access token (and optionally a new refresh token for rotation). If the refresh token is invalid or expired, it returns an appropriate error message.
@router.post("/refresh", response_model=Token, summary="Refresh access token")
def refresh_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token_data.refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        # Generate new tokens
        new_access_token = create_access_token(data={"sub": user.email, "role": user.role})
        new_refresh_token = create_refresh_token(data={"sub": user.email})
        return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.post("/logout")
def logout(request: Request, current_user: User = Depends(get_current_user)):
    token = request.headers.get("Authorization").replace("Bearer ", "")
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
    jti = payload.get("jti")
    
    # Delete the session from Redis
    redis_client.delete(f"session:{current_user.email}:{jti}")
    
    return {"message": "Logged out successfully"}