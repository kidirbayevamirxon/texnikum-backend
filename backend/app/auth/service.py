from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from database.postgres.models.users import User
from backend.depensies import hash_password
from backend.app.owner.schema.create import UserCreate

from common import auth
from backend.app.auth.exseptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UserNotFound,
)


class AuthService:

    @staticmethod
    async def login(data: UserCreate, db: AsyncSession):
        clean_login = data.login.strip()
        stmt = select(User).where(User.login == clean_login)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not auth.verify_password(data.password, user.password):
            raise InvalidCredentialsException()

        tokens = auth.create_tokens(subject=str(user.id))

        return {
            "access_token": tokens["accessToken"],
            "refresh_token": tokens["refreshToken"],
        }
