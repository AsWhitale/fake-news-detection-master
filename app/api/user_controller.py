from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.schemas.response import BaseResponse
from app.services.user_service import UserService

router = APIRouter(tags=["authentication"])


@router.post("/register", response_model=BaseResponse)
async def register(user: UserCreate, user_service: UserService = Depends()):
    result = await user_service.create_user(user)
    return result


@router.post("/login", response_model=BaseResponse)
async def login(login_data: UserLogin, user_service: UserService = Depends()):
    result = await user_service.authenticate_user(login_data.username, login_data.password)
    return result
