import time

from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from app.exceptions.user_exceptions import DuplicateEmailError, DuplicateUsernameError, NonexistentUsernameError, \
    WrongPasswordError
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.response import success_response

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class UserService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db


    async def create_user(self, user: UserCreate):
        # 检查邮箱是否已存在
        if self.db.query(User).filter(User.email == user.email).first():
            raise DuplicateEmailError(user.email)

        # 检查用户名是否已存在
        if self.db.query(User).filter(User.username == user.username).first():
            raise DuplicateUsernameError(user.username)

        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="注册信息冲突"
            ) from IntegrityError

        return success_response(
            data = {
                "id": db_user.id,
                "username": db_user.username,
                "email": db_user.email
            }
        )


    async def authenticate_user(self, username: str, password: str):
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise NonexistentUsernameError(username)
        if not verify_password(password, user.hashed_password):
            raise WrongPasswordError(username)
        return success_response(
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        )
