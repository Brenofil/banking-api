"""
Account models
"""
from datetime import datetime
from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    """Base account model"""
    account_type: str = Field(..., description="Type of account (checking, savings)")
    currency: str = Field(default="USD", description="Account currency")


class AccountCreate(AccountBase):
    """Account creation model"""
    user_id: int


class Account(AccountBase):
    """Account response model"""
    id: int
    account_number: str
    balance: float
    user_id: int
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


