"""
app/repositories/profession_activity_repository.py
----------------------------------------------------
Repository untuk tabel profession_activities.
Diurutkan berdasarkan sort_order ASC.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profession_activity import ProfessionActivity


class ProfessionActivityRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_profession(self, profession_id: int) -> list[ProfessionActivity]:
        result = await self.db.execute(
            select(ProfessionActivity)
            .where(ProfessionActivity.profession_id == profession_id)
            .order_by(ProfessionActivity.sort_order)
        )
        return result.scalars().all()

    async def get_by_id(self, activity_id: int) -> Optional[ProfessionActivity]:
        result = await self.db.execute(
            select(ProfessionActivity).where(ProfessionActivity.id == activity_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self, profession_id: int, description: str, sort_order: int
    ) -> ProfessionActivity:
        now = datetime.now(timezone.utc)
        obj = ProfessionActivity(
            profession_id=profession_id,
            description=description,
            sort_order=sort_order,
            created_at=now,
            updated_at=now,
        )
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(
        self,
        activity_id: int,
        description: Optional[str] = None,
        sort_order: Optional[int] = None,
    ) -> Optional[ProfessionActivity]:
        obj = await self.get_by_id(activity_id)
        if not obj:
            return None
        if description is not None:
            obj.description = description
        if sort_order is not None:
            obj.sort_order = sort_order
        obj.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return obj

    async def delete(self, activity_id: int) -> bool:
        result = await self.db.execute(
            delete(ProfessionActivity).where(ProfessionActivity.id == activity_id)
        )
        return result.rowcount > 0
