from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database.postgres.models.teacher import Teacher
from database.postgres.models.news import New
from database.postgres.models.categories import Category
from database.postgres.models.deficiency import Deficiency

from backend.app.owner.schema.create import (
    TeacherCreate,
    TeacherUpdate,
    NewsCreate,
    NewsUpdate,
    CategoryCreate,
    CategoryUpdate,
    DeficiencyCreate,
    DeficiencyUpdate,
)


class OwnerService:

    # ================= TEACHERS =================
    @staticmethod
    async def teacher_create(
        data: TeacherCreate,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        photo_val = data.photo_url or getattr(data, "photo", None)
        teacher = Teacher(
            first_name=data.first_name.strip(),
            last_name=data.last_name.strip(),
            middle_name=data.middle_name.strip() if data.middle_name else None,
            photo=photo_val,
        )

        db.add(teacher)
        await db.commit()
        await db.refresh(teacher)

        return {"message": "succesfully", "id": teacher.id}

    @staticmethod
    async def teacher_list(
        db: AsyncSession,
        page: int = 1,
        limit: int = 100,
    ):
        if page < 1 or limit < 1:
            raise HTTPException(status_code=400, detail="Noto'g'ri sahifalash parametrlari")

        offset = (page - 1) * limit

        stmt = (
            select(Teacher)
            .offset(offset)
            .limit(limit)
            .order_by(Teacher.id.desc())
        )

        result = await db.execute(stmt)
        teachers = result.scalars().all()
        return [
            {
                "id": t.id,
                "first_name": t.first_name,
                "last_name": t.last_name,
                "middle_name": t.middle_name,
                "photo": [t.photo] if t.photo else [],
                "photo_url": t.photo,
            }
            for t in teachers
        ]

    @staticmethod
    async def teacher_update(
        teacher_id: int,
        data: TeacherUpdate,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        teacher = await db.get(Teacher, teacher_id)
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Xodim topilmadi",
            )

        update_data = data.model_dump(exclude_unset=True)
        if "photo_url" in update_data:
            update_data["photo"] = update_data.pop("photo_url")
        elif "photo" in update_data:
            p = update_data["photo"]
            update_data["photo"] = p[0] if isinstance(p, list) and p else p

        for field, value in update_data.items():
            if hasattr(teacher, field):
                setattr(teacher, field, value)

        await db.commit()
        await db.refresh(teacher)

        return {
            "id": teacher.id,
            "first_name": teacher.first_name,
            "last_name": teacher.last_name,
            "middle_name": teacher.middle_name,
            "photo": [teacher.photo] if teacher.photo else [],
            "photo_url": teacher.photo,
        }

    @staticmethod
    async def teacher_delete(
        teacher_id: int,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        teacher = await db.get(Teacher, teacher_id)
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Xodim topilmadi",
            )

        await db.delete(teacher)
        await db.commit()

        return {"message": "deleted successfully"}

    # ================= NEWS =================
    @staticmethod
    async def news_create(
        data: NewsCreate,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        photo_val = data.photo[0] if isinstance(data.photo, list) and data.photo else data.photo
        news = New(
            description=data.description.strip(),
            photo=photo_val,
        )

        db.add(news)
        await db.commit()
        await db.refresh(news)
        return {"message": "succesfully", "id": news.id}

    @staticmethod
    async def news_list(
        db: AsyncSession,
        page: int = 1,
        limit: int = 100,
    ):
        offset = (page - 1) * limit

        stmt = (
            select(New)
            .order_by(New.created_date.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await db.execute(stmt)
        news_items = result.scalars().all()
        return [
            {
                "id": n.id,
                "description": n.description,
                "photo": [n.photo] if n.photo else [],
                "created_date": n.created_date,
                "updated_date": n.updated_date,
            }
            for n in news_items
        ]

    @staticmethod
    async def news_update(
        news_id: int,
        data: NewsUpdate,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        news = await db.get(New, news_id)
        if not news:
            raise HTTPException(status_code=404, detail="Yangilik topilmadi")

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        if "photo" in update_data:
            p = update_data["photo"]
            update_data["photo"] = p[0] if isinstance(p, list) and p else p

        for field, value in update_data.items():
            if hasattr(news, field):
                setattr(news, field, value)

        await db.commit()
        await db.refresh(news)

        return {"message": "succesfully"}

    @staticmethod
    async def news_delete(
        news_id: int,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        news = await db.get(New, news_id)
        if not news:
            raise HTTPException(status_code=404, detail="Yangilik topilmadi")

        await db.delete(news)
        await db.commit()
        return {"message": "deleted successfully"}

    # ================= CATEGORIES =================
    @staticmethod
    async def category_create(
        data: CategoryCreate,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        name = data.name.strip()
        stmt = select(Category).where(Category.name == name)
        res = await db.execute(stmt)
        if res.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bu nomdagi fakultet allaqachon mavjud",
            )

        category = Category(name=name)
        db.add(category)
        try:
            await db.commit()
            await db.refresh(category)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bu nomdagi fakultet allaqachon mavjud",
            )

        return {"message": "succesfully", "id": category.id, "name": category.name}

    @staticmethod
    async def category_list(
        db: AsyncSession,
        page: int = 1,
        limit: int = 100,
    ):
        offset = (page - 1) * limit

        stmt = (
            select(Category)
            .order_by(Category.id.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def category_update(
        category_id: int,
        data: CategoryUpdate,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        category = await db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Fakultet topilmadi")

        update_data = data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="O'zgartirish uchun ma'lumot kiritilmadi",
            )

        if "name" in update_data and update_data["name"]:
            name = update_data["name"].strip()
            stmt = select(Category).where(Category.name == name, Category.id != category_id)
            res = await db.execute(stmt)
            if res.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Bu nomdagi fakultet allaqachon mavjud",
                )
            category.name = name

        try:
            await db.commit()
            await db.refresh(category)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bu nomdagi fakultet allaqachon mavjud",
            )

        return {"message": "succesfully"}

    @staticmethod
    async def category_delete(
        category_id: int,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        category = await db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Fakultet topilmadi")

        await db.delete(category)
        await db.commit()

        return {"message": "deleted successfully"}

    # ================= DEFICIENCY (YUTUQLAR) =================
    @staticmethod
    async def deficiency_create(
        data: DeficiencyCreate,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        desc = (data.description or getattr(data, "title", "") or "").strip()
        if not desc:
            raise HTTPException(status_code=400, detail="Tavsif kiritilishi shart")

        photo_val = data.photo[0] if isinstance(data.photo, list) and data.photo else data.photo
        deficiency = Deficiency(
            description=desc,
            photo=photo_val,
        )

        db.add(deficiency)
        await db.commit()
        await db.refresh(deficiency)
        return {"message": "succesfully", "id": deficiency.id}

    @staticmethod
    async def deficiency_list(
        db: AsyncSession,
        page: int = 1,
        limit: int = 100,
    ):
        offset = (page - 1) * limit

        stmt = (
            select(Deficiency)
            .order_by(Deficiency.created_date.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await db.execute(stmt)
        items = result.scalars().all()
        return [
            {
                "id": d.id,
                "title": d.description,
                "description": d.description,
                "photo": [d.photo] if d.photo else [],
                "created_date": d.created_date,
                "updated_date": d.updated_date,
            }
            for d in items
        ]

    @staticmethod
    async def deficiency_update(
        deficiency_id: int,
        data: DeficiencyUpdate,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        deficiency = await db.get(Deficiency, deficiency_id)
        if not deficiency:
            raise HTTPException(status_code=404, detail="Yutuq topilmadi")

        update_data = data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            raise HTTPException(status_code=400, detail="Yangilash uchun ma'lumot berilmadi")

        if "photo" in update_data:
            p = update_data["photo"]
            update_data["photo"] = p[0] if isinstance(p, list) and p else p

        for field, value in update_data.items():
            if hasattr(deficiency, field):
                setattr(deficiency, field, value)

        await db.commit()
        await db.refresh(deficiency)
        return deficiency

    @staticmethod
    async def deficiency_delete(
        deficiency_id: int,
        db: AsyncSession,
        current_user,
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

        deficiency = await db.get(Deficiency, deficiency_id)
        if not deficiency:
            raise HTTPException(status_code=404, detail="Yutuq topilmadi")

        await db.delete(deficiency)
        await db.commit()
        return {"message": "deleted successfully"}
