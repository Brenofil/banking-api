"""
Transaction models
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    """Base transaction model"""
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    """Transaction creation model"""
    from_account_id: int
    to_account_id: int


class Transaction(TransactionBase):
    """Transaction response model"""
    id: int
    from_account_id: int
    to_account_id: int
    transaction_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DepositRequest(BaseModel):
    """Deposit request model"""
    account_id: int
    amount: float = Field(..., gt=0, description="Deposit amount (must be positive)")
    description: Optional[str] = "Deposit"


class WithdrawalRequest(BaseModel):
    """Withdrawal request model"""
    account_id: int
    amount: float = Field(..., gt=0, description="Withdrawal amount (must be positive)")
    description: Optional[str] = "Withdrawal"


