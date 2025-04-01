from fastapi import status

class AppException(Exception):
    """基础业务异常"""
    def __init__(self, 
        error_code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict = None
    ):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.details = details