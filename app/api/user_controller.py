from fastapi import APIRouter, Depends

from app.schemas.response import BaseResponse
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import UserService

router = APIRouter(tags=["authentication"])


@router.post("/register", response_model=BaseResponse)
async def register(user: UserCreate, user_service: UserService = Depends()):
    return await user_service.create_user(user)


@router.post("/login", response_model=BaseResponse)
async def login(login_data: UserLogin, user_service: UserService = Depends()):
    return await user_service.authenticate_user(login_data.username, login_data.password)
