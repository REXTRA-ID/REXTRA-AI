"""
app/repositories/study_program_repository.py
----------------------------------------------
Repository untuk tabel study_programs (master).
Termasuk operasi pada pivot profession_study_program_rels.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.study_program import StudyProgram
from app.models.profession_study_program_rel import ProfessionStudyProgramRel


class StudyProgramRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ── Master study_programs ──────────────────────────────────────────────────

    async def get_all(self) -> list[StudyProgram]:
        result = await self.db.execute(select(StudyProgram).order_by(StudyProgram.name))
        return result.scalars().all()

    async def get_by_id(self, sp_id: int) -> Optional[StudyProgram]:
        result = await self.db.execute(select(StudyProgram).where(StudyProgram.id == sp_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[StudyProgram]:
        result = await self.db.execute(select(StudyProgram).where(StudyProgram.name == name))
        return result.scalar_one_or_none()

    async def create(self, name: str) -> StudyProgram:
        now = datetime.now(timezone.utc)
        obj = StudyProgram(name=name, created_at=now, updated_at=now)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def delete(self, sp_id: int) -> bool:
        """RESTRICT — gagal jika masih ada relasi ke profesi."""
        result = await self.db.execute(delete(StudyProgram).where(StudyProgram.id == sp_id))
        return result.rowcount > 0

    # ── Pivot profession_study_program_rels ────────────────────────────────────

    async def get_by_profession(self, profession_id: int) -> list[ProfessionStudyProgramRel]:
        result = await self.db.execute(
            select(ProfessionStudyProgramRel).where(
                ProfessionStudyProgramRel.profession_id == profession_id
            )
        )
        return result.scalars().all()

    async def add_to_profession(
        self, profession_id: int, study_program_id: int
    ) -> ProfessionStudyProgramRel:
        now = datetime.now(timezone.utc)
        obj = ProfessionStudyProgramRel(
            profession_id=profession_id,
            study_program_id=study_program_id,
            created_at=now,
            updated_at=now,
        )
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def remove_from_profession(
        self, profession_id: int, study_program_id: int
    ) -> bool:
        result = await self.db.execute(
            delete(ProfessionStudyProgramRel).where(
                ProfessionStudyProgramRel.profession_id == profession_id,
                ProfessionStudyProgramRel.study_program_id == study_program_id,
            )
        )
        return result.rowcount > 0
