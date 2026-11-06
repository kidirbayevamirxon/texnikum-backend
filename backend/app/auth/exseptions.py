from fastapi import HTTPException, status


class AuthException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(AuthException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Bu loginli foydalanuvchi allaqachon mavjud"


class InvalidCredentialsException(AuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Login yoki parol noto'g'ri"


class UserNotFound(AuthException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Foydalanuvchi topilmadi"
