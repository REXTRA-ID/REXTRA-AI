"""
app/repositories/profession_main_category_repository.py
---------------------------------------------------------
Repository untuk tabel profession_main_categories.

Aturan hard delete: validasi relasi sub_category sebelum delete
dilakukan di service layer, bukan di sini.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profession_main_category import ProfessionMainCategory


class ProfessionMainCategoryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[ProfessionMainCategory]:
        result = await self.db.execute(select(ProfessionMainCategory))
        return result.scalars().all()

    async def get_by_id(self, category_id: int) -> Optional[ProfessionMainCategory]:
        result = await self.db.execute(
            select(ProfessionMainCategory).where(ProfessionMainCategory.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Optional[ProfessionMainCategory]:
        result = await self.db.execute(
            select(ProfessionMainCategory).where(ProfessionMainCategory.code == code)
        )
        return result.scalar_one_or_none()

    async def create(self, code: str, name: str, description: str) -> ProfessionMainCategory:
        now = datetime.now(timezone.utc)
        obj = ProfessionMainCategory(
            code=code,
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
        )
        self.db.add(obj)
        await self.db.flush()  # flush agar id terisi, commit dilakukan eksplisit di service layer
        return obj

    async def update(
        self,
        category_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[ProfessionMainCategory]:
        obj = await self.get_by_id(category_id)
        if not obj:
            return None
        if name is not None:
            obj.name = name
        if description is not None:
            obj.description = description
        obj.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return obj

    async def delete(self, category_id: int) -> bool:
        """Hard delete. Pastikan tidak ada sub_category terkait sebelum memanggil ini."""
        result = await self.db.execute(
            delete(ProfessionMainCategory).where(ProfessionMainCategory.id == category_id)
        )
        return result.rowcount > 0
