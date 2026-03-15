"""
app/repositories/profession_alias_repository.py
-------------------------------------------------
Repository untuk tabel profession_aliases.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profession_alias import ProfessionAlias


class ProfessionAliasRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_profession(self, profession_id: int) -> list[ProfessionAlias]:
        result = await self.db.execute(
            select(ProfessionAlias).where(ProfessionAlias.profession_id == profession_id)
        )
        return result.scalars().all()

    async def get_by_alias_name(self, alias_name: str) -> Optional[ProfessionAlias]:
        """Dipakai di search pipeline untuk resolve alias → profession."""
        result = await self.db.execute(
            select(ProfessionAlias).where(ProfessionAlias.alias_name == alias_name)
        )
        return result.scalar_one_or_none()

    async def create(self, profession_id: int, alias_name: str) -> ProfessionAlias:
        now = datetime.now(timezone.utc)
        obj = ProfessionAlias(
            profession_id=profession_id,
            alias_name=alias_name,
            created_at=now,
            updated_at=now,
        )
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def delete(self, alias_id: int) -> bool:
        result = await self.db.execute(
            delete(ProfessionAlias).where(ProfessionAlias.id == alias_id)
        )
        return result.rowcount > 0

    async def delete_by_profession(self, profession_id: int) -> int:
        """Hapus semua alias milik satu profesi. Kembalikan jumlah baris terhapus."""
        result = await self.db.execute(
            delete(ProfessionAlias).where(ProfessionAlias.profession_id == profession_id)
        )
        return result.rowcount
