# Compatibility alias for exseptions.py
from backend.app.auth.exseptions import (
    AuthException,
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UserNotFound,
)

__all__ = [
    "AuthException",
    "UserAlreadyExistsException",
    "InvalidCredentialsException",
    "UserNotFound",
]
