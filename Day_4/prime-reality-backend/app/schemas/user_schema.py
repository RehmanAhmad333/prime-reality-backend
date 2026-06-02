from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    role: Optional[str] = "buyer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    role: str
    is_active: bool

    class Config:
        from_attributes = True  # Yeh setting Pydantic ko batati hai ke wo SQLAlchemy model ke attributes se data le, na ke dict keys se. Iska matlab hai ke agar aapka User model me id, email, full_name, phone, role, aur is_active attributes hain, to Pydantic unhi attributes ko use karke UserResponse schema ko populate karega. Yeh especially tab useful hota hai jab aap SQLAlchemy models ko directly response me return karte hain, taki aapko manually data ko dict me convert karne ki zarurat na pade.

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None