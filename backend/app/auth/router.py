from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends,status

from database.postgres.database import get_async_db
from backend.app.auth.service import AuthService
from backend.app.owner.schema.create import UserCreate

router = APIRouter(prefix="/auth", tags=["AUTH"])


@router.post("/login")
async def login(data:UserCreate, db:AsyncSession = Depends(get_async_db)):
    return await AuthService.login(data=data,db=db)
