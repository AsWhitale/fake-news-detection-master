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

class DuplicateEmailError(AppException):
    """邮箱重复异常"""
    def __init__(self, email: str):
        super().__init__(
            error_code="DUPLICATE_EMAIL",
            message="该邮箱已被注册",
            details={"email": email}
        )

class DuplicateUsernameError(AppException):
    """用户名重复异常"""
    def __init__(self, username: str):
        super().__init__(
            error_code="DUPLICATE_USERNAME",
            message="用户名已存在",
            details={"username": username}
        )