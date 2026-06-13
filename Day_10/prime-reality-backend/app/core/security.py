# This module provides security-related functions for the Prime Reality backend application. It includes functions for hashing passwords, verifying passwords, and creating JWT access and refresh tokens. The module uses the Passlib library for secure password hashing and the Python-JOSE library for handling JWTs. The configuration settings for JWT, such as secret keys and expiration times, are loaded from environment variables defined in the app's configuration module.

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import uuid
from app.core.redis import redis_client


# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create refresh token
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        jti = payload.get("jti")
        
        # Check if session exists in Redis
        if not redis_client.exists(f"session:{user_id}:{jti}"):
            raise jwt.JWTError("Session not found or expired")
        
        return payload
    except jwt.JWTError:
        return None




def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Set your desired expiration (e.g., 7 days or None for no expiration)
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    
    # Generate a unique session ID (jti)
    session_id = str(uuid.uuid4())
    to_encode["jti"] = session_id
    
    # Store session in Redis (expires with the token)
    user_id = to_encode.get("sub")
    redis_client.setex(
        f"session:{user_id}:{session_id}",
        expires_delta or timedelta(days=7),
        "active"
    )
    
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return token