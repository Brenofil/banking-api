"""
Account management endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from app.models import Account, AccountCreate
import random
import string

router = APIRouter()

# In-memory storage (replace with database in production)
accounts_db = {}
account_id_counter = 1


def generate_account_number():
    """Generate a random account number"""
    return ''.join(random.choices(string.digits, k=10))


@router.post("/", response_model=Account, status_code=status.HTTP_201_CREATED)
async def create_account(account: AccountCreate):
    """Create a new account"""
    global account_id_counter
    
    from datetime import datetime
    new_account = {
        "id": account_id_counter,
        "account_number": generate_account_number(),
        "account_type": account.account_type,
        "currency": account.currency,
        "balance": 0.0,
        "user_id": account.user_id,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    accounts_db[account_id_counter] = new_account
    account_id_counter += 1
    
    return new_account


@router.get("/", response_model=List[Account])
async def list_accounts(user_id: Optional[int] = None):
    """List all accounts or filter by user_id"""
    if user_id:
        return [acc for acc in accounts_db.values() if acc["user_id"] == user_id]
    return list(accounts_db.values())


@router.get("/{account_id}", response_model=Account)
async def get_account(account_id: int):
    """Get a specific account by ID"""
    if account_id not in accounts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return accounts_db[account_id]


@router.get("/{account_id}/balance")
async def get_balance(account_id: int):
    """Get account balance"""
    if account_id not in accounts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    account = accounts_db[account_id]
    return {
        "account_id": account_id,
        "account_number": account["account_number"],
        "balance": account["balance"],
        "currency": account["currency"]
    }


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_id: int):
    """Delete an account"""
    if account_id not in accounts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    del accounts_db[account_id]
    return None


