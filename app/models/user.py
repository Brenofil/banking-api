"""
User models
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr
    full_name: str
    phone: Optional[str] = None


class UserCreate(UserBase):
    """User creation model"""
    password: str


class User(UserBase):
    """User response model"""
    id: int
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


