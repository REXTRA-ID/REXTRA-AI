"""
app/repositories/profession_career_path_repository.py
-------------------------------------------------------
Repository untuk tabel profession_career_paths.
Diurutkan berdasarkan sort_order ASC.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profession_career_path import ProfessionCareerPath


class ProfessionCareerPathRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_profession(self, profession_id: int) -> list[ProfessionCareerPath]:
        result = await self.db.execute(
            select(ProfessionCareerPath)
            .where(ProfessionCareerPath.profession_id == profession_id)
            .order_by(ProfessionCareerPath.sort_order)
        )
        return result.scalars().all()

    async def get_by_id(self, path_id: int) -> Optional[ProfessionCareerPath]:
        result = await self.db.execute(
            select(ProfessionCareerPath).where(ProfessionCareerPath.id == path_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        profession_id: int,
        title: str,
        experience_range: str,
        sort_order: int,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
    ) -> ProfessionCareerPath:
        now = datetime.now(timezone.utc)
        obj = ProfessionCareerPath(
            profession_id=profession_id,
            title=title,
            experience_range=experience_range,
            salary_min=salary_min,
            salary_max=salary_max,
            sort_order=sort_order,
            created_at=now,
            updated_at=now,
        )
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(
        self,
        path_id: int,
        title: Optional[str] = None,
        experience_range: Optional[str] = None,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        sort_order: Optional[int] = None,
    ) -> Optional[ProfessionCareerPath]:
        obj = await self.get_by_id(path_id)
        if not obj:
            return None
        if title is not None:
            obj.title = title
        if experience_range is not None:
            obj.experience_range = experience_range
        if salary_min is not None:
            obj.salary_min = salary_min
        if salary_max is not None:
            obj.salary_max = salary_max
        if sort_order is not None:
            obj.sort_order = sort_order
        obj.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return obj

    async def delete(self, path_id: int) -> bool:
        result = await self.db.execute(
            delete(ProfessionCareerPath).where(ProfessionCareerPath.id == path_id)
        )
        return result.rowcount > 0
