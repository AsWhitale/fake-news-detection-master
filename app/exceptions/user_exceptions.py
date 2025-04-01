from app.exceptions.base_exceptions import AppException


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

class NonexistentUsernameError(AppException):
    """用户名不存在"""
    def __init__(self, username: str):
        super().__init__(
            error_code="NONEXISTENT_USERNAME",
            message="用户名不存在",
            details={"username": username}
        )

class WrongPasswordError(AppException):
    """密码错误"""
    def __init__(self, username: str):
        super().__init__(
            error_code="WRONG_PASSWORD",
            message="密码错误",
            details={"username": username}
        )