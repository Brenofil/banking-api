"""
User management endpoints
"""
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models import User, UserCreate

router = APIRouter()

# In-memory storage (replace with database in production)
users_db = {}
user_id_counter = 1


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    global user_id_counter
    
    # Check if email already exists
    for existing_user in users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    from datetime import datetime
    new_user = {
        "id": user_id_counter,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    
    return new_user


@router.get("/", response_model=List[User])
async def list_users():
    """List all users"""
    return list(users_db.values())


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users_db[user_id]


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete a user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    del users_db[user_id]
    return None


