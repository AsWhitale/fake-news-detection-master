from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin
from app.schemas.response import BaseResponse
from app.services.auth_service import UserService

router = APIRouter(tags=["authentication"])


@router.post("/register", response_model=BaseResponse)
async def register(user: UserCreate, user_service: UserService = Depends()):
    result = await user_service.create_user(user)
    return result


@router.post("/login", response_model=BaseResponse)
async def login(login_data: UserLogin, service: UserService = Depends()):
    user = service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "登录成功", "result": user}
