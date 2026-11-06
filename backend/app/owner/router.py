from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, Path

from database.postgres.database import get_async_db
from backend.app.owner.service import OwnerService
from backend.depensies import get_current_user
from backend.app.owner.schema.create import (
    TeacherCreate,
    TeacherUpdate,
    NewsCreate,
    NewsUpdate,
    CategoryUpdate,
    CategoryCreate,
    DeficiencyUpdate,
    DeficiencyCreate,
)

router = APIRouter(prefix="/owner", tags=["OWNER"])

# ================= TEACHERS =================
@router.post("/teachers")
async def create_teacher(
    data: TeacherCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.teacher_create(data, db, current_user)


@router.get("/teachers")
async def get_teachers(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_async_db),
):
    return await OwnerService.teacher_list(
        db=db,
        page=page,
        limit=limit,
    )


@router.patch("/teachers/{teacher_id}")
async def update_teacher(
    teacher_id: int = Path(..., ge=1),
    data: TeacherUpdate = ...,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.teacher_update(
        teacher_id=teacher_id,
        data=data,
        db=db,
        current_user=current_user,
    )


@router.delete("/teachers/{teacher_id}")
async def delete_teacher(
    teacher_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.teacher_delete(
        teacher_id=teacher_id,
        db=db,
        current_user=current_user,
    )


# ================= NEWS =================
@router.post("/news")
@router.post("/create_news")
async def create_news(
    data: NewsCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.news_create(data, db, current_user)


@router.get("/news")
async def get_news(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_async_db),
):
    return await OwnerService.news_list(db, page, limit)


@router.patch("/news/{news_id}")
async def update_news(
    news_id: int = Path(..., ge=1),
    data: NewsUpdate = ...,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.news_update(news_id, data, db, current_user)


@router.delete("/news/{news_id}")
async def delete_news(
    news_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.news_delete(news_id, db, current_user)


# ================= CATEGORIES (FAKULTETLAR) =================
@router.post("/categories")
@router.post("/create_categories")
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.category_create(data, db, current_user)


@router.get("/categories")
async def get_categories(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_async_db),
):
    return await OwnerService.category_list(db, page, limit)


@router.patch("/categories/{category_id}")
async def update_category(
    category_id: int = Path(..., ge=1),
    data: CategoryUpdate = ...,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.category_update(
        category_id, data, db, current_user
    )


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.category_delete(
        category_id, db, current_user
    )


# ================= DEFICIENCY (YUTUQLAR) =================
@router.post("/deficiency")
@router.post("/create_deficiency")
async def create_deficiency(
    data: DeficiencyCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.deficiency_create(data, db, current_user)


@router.get("/deficiency")
async def get_deficiencies(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_async_db),
):
    return await OwnerService.deficiency_list(db, page, limit)


@router.patch("/deficiency/{deficiency_id}")
async def update_deficiency(
    deficiency_id: int = Path(..., ge=1),
    data: DeficiencyUpdate = ...,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.deficiency_update(
        deficiency_id, data, db, current_user
    )


@router.delete("/deficiency/{deficiency_id}")
async def delete_deficiency(
    deficiency_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user),
):
    return await OwnerService.deficiency_delete(
        deficiency_id, db, current_user
    )
