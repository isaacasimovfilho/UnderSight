from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import EmailStr

from app.db.session import get_db
from app.core.security import (
    get_current_active_user,
    get_password_hash,
    create_access_token
)
from app.schemas.siem import (
    UserCreate, UserUpdate, UserResponse,
    Token, TokenData
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # TODO: Add DB lookup for existing user
    # existing = db.query(User).filter(User.username == user_data.username).first()
    # if existing:
    #     raise HTTPException(status_code=400, detail="Username already registered")
    
    user = UserResponse(
        id="1",
        username=user_data.username,
        email=user_data.email,
        role=user_data.role or "analyst",
        is_active=True,
        created_at=datetime.utcnow()
    )
    
    return user


@router.post("/login", response_model=Token)
async def login(username: str, password: str, db: Session = Depends(get_db)):
    """Login and get access token."""
    # TODO: Add real authentication
    # user = db.query(User).filter(User.username == username).first()
    # if not user or not verify_password(password, user.password_hash):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Mock user for development
    if username == "admin" and password == "admin":
        access_token = create_access_token(
            data={"sub": username, "user_id": "1"}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_active_user)):
    """Get current user profile."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_me(
    user_data: UserUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    # TODO: Implement update
    return current_user


# Import datetime for the function
from datetime import datetime
