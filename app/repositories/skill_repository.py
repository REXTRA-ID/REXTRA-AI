"""
app/repositories/skill_repository.py
--------------------------------------
Repository untuk tabel skills (master).
Termasuk operasi pada pivot profession_skill_rels.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skill import Skill
from app.models.profession_skill_rel import ProfessionSkillRel, VALID_SKILL_TYPES, VALID_PRIORITIES


class SkillRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ── Master skills ──────────────────────────────────────────────────────────

    async def get_all(self) -> list[Skill]:
        result = await self.db.execute(select(Skill).order_by(Skill.name))
        return result.scalars().all()

    async def get_by_id(self, skill_id: int) -> Optional[Skill]:
        result = await self.db.execute(select(Skill).where(Skill.id == skill_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Skill]:
        result = await self.db.execute(select(Skill).where(Skill.name == name))
        return result.scalar_one_or_none()

    async def create(self, name: str) -> Skill:
        now = datetime.now(timezone.utc)
        obj = Skill(name=name, created_at=now, updated_at=now)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def delete(self, skill_id: int) -> bool:
        """RESTRICT — gagal jika masih ada relasi ke profesi."""
        result = await self.db.execute(delete(Skill).where(Skill.id == skill_id))
        return result.rowcount > 0

    # ── Pivot profession_skill_rels ────────────────────────────────────────────

    async def get_skills_by_profession(self, profession_id: int) -> list[ProfessionSkillRel]:
        result = await self.db.execute(
            select(ProfessionSkillRel).where(ProfessionSkillRel.profession_id == profession_id)
        )
        return result.scalars().all()

    async def add_skill_to_profession(
        self,
        profession_id: int,
        skill_id: int,
        skill_type: str,
        priority: str,
    ) -> ProfessionSkillRel:
        """
        Tambah skill ke profesi.
        Validasi nilai skill_type dan priority dilakukan di service layer
        menggunakan VALID_SKILL_TYPES dan VALID_PRIORITIES dari models.
        """
        now = datetime.now(timezone.utc)
        obj = ProfessionSkillRel(
            profession_id=profession_id,
            skill_id=skill_id,
            skill_type=skill_type,
            priority=priority,
            created_at=now,
            updated_at=now,
        )
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def remove_skill_from_profession(
        self, profession_id: int, skill_id: int
    ) -> bool:
        result = await self.db.execute(
            delete(ProfessionSkillRel).where(
                ProfessionSkillRel.profession_id == profession_id,
                ProfessionSkillRel.skill_id == skill_id,
            )
        )
        return result.rowcount > 0
