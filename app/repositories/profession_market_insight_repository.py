"""
app/repositories/profession_market_insight_repository.py
----------------------------------------------------------
Repository untuk tabel profession_market_insights.
Diurutkan berdasarkan sort_order ASC.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profession_market_insight import ProfessionMarketInsight


class ProfessionMarketInsightRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_profession(self, profession_id: int) -> list[ProfessionMarketInsight]:
        result = await self.db.execute(
            select(ProfessionMarketInsight)
            .where(ProfessionMarketInsight.profession_id == profession_id)
            .order_by(ProfessionMarketInsight.sort_order)
        )
        return result.scalars().all()

    async def get_by_id(self, insight_id: int) -> Optional[ProfessionMarketInsight]:
        result = await self.db.execute(
            select(ProfessionMarketInsight).where(ProfessionMarketInsight.id == insight_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self, profession_id: int, description: str, sort_order: int
    ) -> ProfessionMarketInsight:
        now = datetime.now(timezone.utc)
        obj = ProfessionMarketInsight(
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
        insight_id: int,
        description: Optional[str] = None,
        sort_order: Optional[int] = None,
    ) -> Optional[ProfessionMarketInsight]:
        obj = await self.get_by_id(insight_id)
        if not obj:
            return None
        if description is not None:
            obj.description = description
        if sort_order is not None:
            obj.sort_order = sort_order
        obj.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return obj

    async def delete(self, insight_id: int) -> bool:
        result = await self.db.execute(
            delete(ProfessionMarketInsight).where(ProfessionMarketInsight.id == insight_id)
        )
        return result.rowcount > 0
