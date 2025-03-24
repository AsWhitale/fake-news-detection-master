from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService
from app.database import get_db

router = APIRouter(tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    return UserService.create_user(db, user)

@router.post("/login")
def login(login_data: UserLogin, db: Annotated[Session, Depends(get_db)]):
    user = UserService.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "登录成功"}