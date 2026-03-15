"""
app/repositories/profession_repository.py
-------------------------------------------
Repository untuk tabel professions.

Business rules yang dijaga di SERVICE LAYER (bukan di sini):
    1. sub_category_id HARUS berada di bawah main_category_id yang sama.
    2. slug di-generate otomatis dari name jika tidak diisi:
           slug = name.lower().replace(" ", "-")  → "Data Engineer" → "data-engineer"
    3. Jika riasec_code_id tidak None tapi riasec_description None
       → service layer wajib return error / warning.
    4. Profesi dengan riasec_code_id = None tidak diikutsertakan dalam
       matching RIASEC — filter ini diterapkan di service/query layer.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.profession import Profession

# [FIX-4] Sentinel untuk membedakan "tidak diisi" vs "sengaja di-set None"
_UNSET = object()


class ProfessionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ── READ ──────────────────────────────────────────────────────────────────

    async def get_all(self) -> list[Profession]:
        result = await self.db.execute(select(Profession))
        return result.scalars().all()

    async def get_by_id(self, profession_id: int) -> Optional[Profession]:
        result = await self.db.execute(
            select(Profession).where(Profession.id == profession_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Profession]:
        """Dipakai untuk endpoint publik /professions/{slug}."""
        result = await self.db.execute(
            select(Profession).where(Profession.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_by_id_with_relations(self, profession_id: int) -> Optional[Profession]:
        """
        Load profesi beserta semua relasi turunan dalam 1 query (eager load).
        Gunakan untuk endpoint detail profesi.
        """
        result = await self.db.execute(
            select(Profession)
            .options(
                selectinload(Profession.main_category),
                selectinload(Profession.sub_category),
                selectinload(Profession.aliases),
                selectinload(Profession.activities),
                selectinload(Profession.market_insights),
                selectinload(Profession.career_paths),
                selectinload(Profession.skill_rels),
                selectinload(Profession.tool_rels),
                selectinload(Profession.study_program_rels),
            )
            .where(Profession.id == profession_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug_with_relations(self, slug: str) -> Optional[Profession]:
        """Load profesi by slug beserta semua relasi. Dipakai di endpoint publik."""
        result = await self.db.execute(
            select(Profession)
            .options(
                selectinload(Profession.main_category),
                selectinload(Profession.sub_category),
                selectinload(Profession.aliases),
                selectinload(Profession.activities),
                selectinload(Profession.market_insights),
                selectinload(Profession.career_paths),
                selectinload(Profession.skill_rels),
                selectinload(Profession.tool_rels),
                selectinload(Profession.study_program_rels),
            )
            .where(Profession.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_by_main_category(self, main_category_id: int) -> list[Profession]:
        result = await self.db.execute(
            select(Profession).where(Profession.main_category_id == main_category_id)
        )
        return result.scalars().all()

    async def get_by_sub_category(self, sub_category_id: int) -> list[Profession]:
        result = await self.db.execute(
            select(Profession).where(Profession.sub_category_id == sub_category_id)
        )
        return result.scalars().all()

    async def get_with_riasec(self) -> list[Profession]:
        """Ambil hanya profesi yang memiliki riasec_code_id (untuk matching RIASEC)."""
        result = await self.db.execute(
            select(Profession).where(Profession.riasec_code_id.is_not(None))
        )
        return result.scalars().all()

    # ── WRITE ─────────────────────────────────────────────────────────────────

    async def create(
        self,
        slug: str,
        name: str,
        main_category_id: int,
        sub_category_id: int,
        image_url: Optional[str] = None,
        riasec_code_id: Optional[int] = None,
        about_description: Optional[str] = None,
        riasec_description: Optional[str] = None,
    ) -> Profession:
        now = datetime.now(timezone.utc)
        obj = Profession(
            slug=slug,
            name=name,
            main_category_id=main_category_id,
            sub_category_id=sub_category_id,
            image_url=image_url,
            riasec_code_id=riasec_code_id,
            about_description=about_description,
            riasec_description=riasec_description,
            created_at=now,
            updated_at=now,
        )
        self.db.add(obj)
        await self.db.flush()  # id terisi setelah flush
        return obj

    async def update(
        self,
        profession_id: int,
        slug=_UNSET,                  # [FIX-4] pakai sentinel, bukan Optional
        name=_UNSET,
        image_url=_UNSET,             # [FIX-4] bisa di-set ke None untuk hapus gambar
        main_category_id=_UNSET,
        sub_category_id=_UNSET,
        riasec_code_id=_UNSET,        # [FIX-4] bisa di-set ke None untuk hapus RIASEC
        about_description=_UNSET,     # [FIX-4] bisa di-set ke None
        riasec_description=_UNSET,    # [FIX-4] bisa di-set ke None
    ) -> Optional[Profession]:
        obj = await self.get_by_id(profession_id)
        if not obj:
            return None
        # [FIX-4] Cek sentinel _UNSET, bukan None — agar bisa set field ke None secara sengaja
        if slug is not _UNSET:
            obj.slug = slug
        if name is not _UNSET:
            obj.name = name
        if image_url is not _UNSET:
            obj.image_url = image_url
        if main_category_id is not _UNSET:
            obj.main_category_id = main_category_id
        if sub_category_id is not _UNSET:
            obj.sub_category_id = sub_category_id
        if riasec_code_id is not _UNSET:
            obj.riasec_code_id = riasec_code_id
        if about_description is not _UNSET:
            obj.about_description = about_description
        if riasec_description is not _UNSET:
            obj.riasec_description = riasec_description
        obj.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return obj

    async def delete(self, profession_id: int) -> bool:
        """
        Hard delete. Relasi turunan (aliases, activities, dsb) ter-delete otomatis
        via CASCADE yang sudah ada di DB.
        """
        result = await self.db.execute(
            delete(Profession).where(Profession.id == profession_id)
        )
        return result.rowcount > 0
