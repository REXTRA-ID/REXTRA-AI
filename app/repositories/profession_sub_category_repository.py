"""
app/repositories/profession_sub_category_repository.py
--------------------------------------------------------
Repository untuk tabel profession_sub_categories.

Business rule penting (dijaga di service layer, bukan di sini):
    Setiap sub_category HANYA dimiliki oleh 1 main_category.
    Validasi konsistensi sub_category ↔ main_category dilakukan
    di service layer sebelum memanggil create/update.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profession_sub_category import ProfessionSubCategory


class ProfessionSubCategoryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[ProfessionSubCategory]:
        result = await self.db.execute(select(ProfessionSubCategory))
        return result.scalars().all()

    async def get_by_id(self, sub_id: int) -> Optional[ProfessionSubCategory]:
        result = await self.db.execute(
            select(ProfessionSubCategory).where(ProfessionSubCategory.id == sub_id)
        )
        return result.scalar_one_or_none()

    async def get_by_main_category(self, main_category_id: int) -> list[ProfessionSubCategory]:
        result = await self.db.execute(
            select(ProfessionSubCategory).where(
                ProfessionSubCategory.main_category_id == main_category_id
            )
        )
        return result.scalars().all()

    async def get_by_main_and_code(
        self, main_category_id: int, code: str
    ) -> Optional[ProfessionSubCategory]:
        result = await self.db.execute(
            select(ProfessionSubCategory).where(
                ProfessionSubCategory.main_category_id == main_category_id,
                ProfessionSubCategory.code == code,
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        main_category_id: int,
        code: str,
        name: str,
        description: str,
    ) -> ProfessionSubCategory:
        now = datetime.now(timezone.utc)
        obj = ProfessionSubCategory(
            main_category_id=main_category_id,
            code=code,
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
        )
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(
        self,
        sub_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[ProfessionSubCategory]:
        obj = await self.get_by_id(sub_id)
        if not obj:
            return None
        if name is not None:
            obj.name = name
        if description is not None:
            obj.description = description
        obj.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return obj

    async def delete(self, sub_id: int) -> bool:
        result = await self.db.execute(
            delete(ProfessionSubCategory).where(ProfessionSubCategory.id == sub_id)
        )
        return result.rowcount > 0
