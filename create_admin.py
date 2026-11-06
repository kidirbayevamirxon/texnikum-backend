import asyncio
import sys
from sqlalchemy import select
from database.postgres.database import AsyncSessionLocal
from database.postgres.models.users import User
from common import auth

async def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "admin"
    password = sys.argv[2] if len(sys.argv) > 2 else "admin123"

    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.login == login)
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print(f"Foydalanuvchi '{login}' allaqachon mavjud! ID: {existing_user.id}")
            return

        hashed_password = auth.hash_password(password)
        new_user = User(login=login, password=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        print(f"Muvaffaqiyatli yaratildi! ID: {new_user.id}, Login: {new_user.login}")

if __name__ == "__main__":
    asyncio.run(main())

