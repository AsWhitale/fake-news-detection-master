from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
import time

from starlette.responses import JSONResponse

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    status: int
    message: str
    data: Optional[T] = None
    timestamp: int = int(time.time())

class ErrorDetail(BaseModel):
    code: str  # 业务错误码 (如 "AUTH_FAILED")
    details: Optional[dict] = None

class ErrorResponse(BaseResponse[None]):
    error: ErrorDetail

from fastapi import APIRouter, status

router = APIRouter(default_response_class=JSONResponse)

def success_response(
    data: any = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK
):
    return {
        "status": status_code,
        "message": message,
        "data": data,
        "timestamp": int(time.time())
    }

def error_response(
    message: str,
    error_code: str,
    status_code: int = 400,
    details: dict = None
):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message,
            "error": {
                "code": error_code,
                "details": details
            },
            "timestamp": int(time.time())
        }
    )