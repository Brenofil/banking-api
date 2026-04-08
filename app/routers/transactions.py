"""
Transaction management endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from app.models import Transaction, TransactionCreate, DepositRequest, WithdrawalRequest
from app.routers.accounts import accounts_db

router = APIRouter()

# In-memory storage (replace with database in production)
transactions_db = {}
transaction_id_counter = 1


@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction: TransactionCreate):
    """Create a new transaction (transfer between accounts)"""
    global transaction_id_counter
    
    # Validate accounts exist
    if transaction.from_account_id not in accounts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source account not found"
        )
    if transaction.to_account_id not in accounts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination account not found"
        )
    
    from_account = accounts_db[transaction.from_account_id]
    to_account = accounts_db[transaction.to_account_id]
    
    # Check sufficient balance
    if from_account["balance"] < transaction.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )
    
    # Perform transaction
    from_account["balance"] -= transaction.amount
    to_account["balance"] += transaction.amount
    
    from datetime import datetime
    new_transaction = {
        "id": transaction_id_counter,
        "from_account_id": transaction.from_account_id,
        "to_account_id": transaction.to_account_id,
        "amount": transaction.amount,
        "description": transaction.description,
        "transaction_type": "transfer",
        "status": "completed",
        "created_at": datetime.utcnow()
    }
    
    transactions_db[transaction_id_counter] = new_transaction
    transaction_id_counter += 1
    
    return new_transaction


@router.post("/deposit", response_model=Transaction, status_code=status.HTTP_201_CREATED)
async def deposit(deposit_request: DepositRequest):
    """Deposit money into an account"""
    global transaction_id_counter
    
    if deposit_request.account_id not in accounts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    account = accounts_db[deposit_request.account_id]
    account["balance"] += deposit_request.amount
    
    from datetime import datetime
    new_transaction = {
        "id": transaction_id_counter,
        "from_account_id": 0,  # 0 represents external source
        "to_account_id": deposit_request.account_id,
        "amount": deposit_request.amount,
        "description": deposit_request.description,
        "transaction_type": "deposit",
        "status": "completed",
        "created_at": datetime.utcnow()
    }
    
    transactions_db[transaction_id_counter] = new_transaction
    transaction_id_counter += 1
    
    return new_transaction


@router.post("/withdraw", response_model=Transaction, status_code=status.HTTP_201_CREATED)
async def withdraw(withdrawal_request: WithdrawalRequest):
    """Withdraw money from an account"""
    global transaction_id_counter
    
    if withdrawal_request.account_id not in accounts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    account = accounts_db[withdrawal_request.account_id]
    
    if account["balance"] < withdrawal_request.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )
    
    account["balance"] -= withdrawal_request.amount
    
    from datetime import datetime
    new_transaction = {
        "id": transaction_id_counter,
        "from_account_id": withdrawal_request.account_id,
        "to_account_id": 0,  # 0 represents external destination
        "amount": withdrawal_request.amount,
        "description": withdrawal_request.description,
        "transaction_type": "withdrawal",
        "status": "completed",
        "created_at": datetime.utcnow()
    }
    
    transactions_db[transaction_id_counter] = new_transaction
    transaction_id_counter += 1
    
    return new_transaction


@router.get("/", response_model=List[Transaction])
async def list_transactions(account_id: Optional[int] = None):
    """List all transactions or filter by account_id"""
    if account_id:
        return [
            txn for txn in transactions_db.values()
            if txn["from_account_id"] == account_id or txn["to_account_id"] == account_id
        ]
    return list(transactions_db.values())


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int):
    """Get a specific transaction by ID"""
    if transaction_id not in transactions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transactions_db[transaction_id]


