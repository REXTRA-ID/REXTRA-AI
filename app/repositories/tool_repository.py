"""
app/repositories/tool_repository.py
-------------------------------------
Repository untuk tabel tools (master).
Termasuk operasi pada pivot profession_tool_rels.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tool import Tool
from app.models.profession_tool_rel import ProfessionToolRel, VALID_USAGE_TYPES


class ToolRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ── Master tools ───────────────────────────────────────────────────────────

    async def get_all(self) -> list[Tool]:
        result = await self.db.execute(select(Tool).order_by(Tool.name))
        return result.scalars().all()

    async def get_by_id(self, tool_id: int) -> Optional[Tool]:
        result = await self.db.execute(select(Tool).where(Tool.id == tool_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Tool]:
        result = await self.db.execute(select(Tool).where(Tool.name == name))
        return result.scalar_one_or_none()

    async def create(self, name: str) -> Tool:
        now = datetime.now(timezone.utc)
        obj = Tool(name=name, created_at=now, updated_at=now)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def delete(self, tool_id: int) -> bool:
        """RESTRICT — gagal jika masih ada relasi ke profesi."""
        result = await self.db.execute(delete(Tool).where(Tool.id == tool_id))
        return result.rowcount > 0

    # ── Pivot profession_tool_rels ─────────────────────────────────────────────

    async def get_tools_by_profession(self, profession_id: int) -> list[ProfessionToolRel]:
        result = await self.db.execute(
            select(ProfessionToolRel).where(ProfessionToolRel.profession_id == profession_id)
        )
        return result.scalars().all()

    async def add_tool_to_profession(
        self,
        profession_id: int,
        tool_id: int,
        usage_type: str,
    ) -> ProfessionToolRel:
        """
        Tambah tool ke profesi.
        Validasi nilai usage_type dilakukan di service layer
        menggunakan VALID_USAGE_TYPES dari models.
        """
        now = datetime.now(timezone.utc)
        obj = ProfessionToolRel(
            profession_id=profession_id,
            tool_id=tool_id,
            usage_type=usage_type,
            created_at=now,
            updated_at=now,
        )
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def remove_tool_from_profession(
        self, profession_id: int, tool_id: int
    ) -> bool:
        result = await self.db.execute(
            delete(ProfessionToolRel).where(
                ProfessionToolRel.profession_id == profession_id,
                ProfessionToolRel.tool_id == tool_id,
            )
        )
        return result.rowcount > 0
