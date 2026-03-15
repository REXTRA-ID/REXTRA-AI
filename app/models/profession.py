"""
app/models/profession.py
-------------------------
Entity  : professions
Relasi  :
    (N) → (1) profession_main_categories  via main_category_id
    (N) → (1) profession_sub_categories   via sub_category_id
    (N) → (1) riasec_codes                via riasec_code_id  [nullable]
    (1) → (N) profession_aliases
    (1) → (N) profession_activities
    (1) → (N) profession_market_insights
    (1) → (N) profession_career_paths
    (N) ↔ (N) skills       via profession_skill_rels
    (N) ↔ (N) tools        via profession_tool_rels
    (N) ↔ (N) study_programs via profession_study_program_rels

Catatan kolom:
    slug             → public identifier di URL (/professions/data-engineer), UNIQUE
    riasec_code_id   → nullable; profesi tanpa nilai ini tidak ikut matching RIASEC
    riasec_description → wajib diisi bersamaan saat riasec_code_id diisi (validasi di service)
    image_url, about_description, riasec_description → nullable (isi bertahap)

⚠️  Akses DB:
    Tabel sudah ada di PostgreSQL online (103.171.84.248:5433/rextra).
    Model ini HANYA merefleksikan tabel — tidak membuat atau mengubah tabel.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.profession_main_category import ProfessionMainCategory
    from app.models.profession_sub_category import ProfessionSubCategory
    from app.models.profession_alias import ProfessionAlias
    from app.models.profession_activity import ProfessionActivity
    from app.models.profession_market_insight import ProfessionMarketInsight
    from app.models.profession_career_path import ProfessionCareerPath
    from app.models.profession_skill_rel import ProfessionSkillRel
    from app.models.profession_tool_rel import ProfessionToolRel
    from app.models.profession_study_program_rel import ProfessionStudyProgramRel
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Profession(Base):
    __tablename__ = "professions"

    # ── Kolom ─────────────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Public identifier untuk URL — generate otomatis dari name di service layer
    # Contoh: "Data Engineer" → "data-engineer"
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    main_category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profession_main_categories.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    sub_category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profession_sub_categories.id", ondelete="RESTRICT"), nullable=False, index=True
    )

    # Nullable FK ke riasec_codes — profesi tanpa nilai ini tidak ikut matching RIASEC
    riasec_code_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("riasec_codes.id", ondelete="RESTRICT"), nullable=True, index=True
    )

    about_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Wajib diisi bersamaan dengan riasec_code_id — validasi di service layer
    riasec_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # [FIX-3]
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # [FIX-3]

    # ── Relasi ────────────────────────────────────────────────────────────────
    # [FIX-2] Ditambahkan back_populates="professions" — sebelumnya tidak ada
    main_category: Mapped["ProfessionMainCategory"] = relationship(
        "ProfessionMainCategory", back_populates="professions", lazy="select"
    )
    sub_category: Mapped["ProfessionSubCategory"] = relationship(
        "ProfessionSubCategory", back_populates="professions", lazy="select"
    )

    aliases: Mapped[list["ProfessionAlias"]] = relationship(
        "ProfessionAlias", back_populates="profession",
        cascade="all, delete-orphan", lazy="select",
    )
    activities: Mapped[list["ProfessionActivity"]] = relationship(
        "ProfessionActivity", back_populates="profession",
        cascade="all, delete-orphan", order_by="ProfessionActivity.sort_order", lazy="select",
    )
    market_insights: Mapped[list["ProfessionMarketInsight"]] = relationship(
        "ProfessionMarketInsight", back_populates="profession",
        cascade="all, delete-orphan", order_by="ProfessionMarketInsight.sort_order", lazy="select",
    )
    career_paths: Mapped[list["ProfessionCareerPath"]] = relationship(
        "ProfessionCareerPath", back_populates="profession",
        cascade="all, delete-orphan", order_by="ProfessionCareerPath.sort_order", lazy="select",
    )
    skill_rels: Mapped[list["ProfessionSkillRel"]] = relationship(
        "ProfessionSkillRel", back_populates="profession",
        cascade="all, delete-orphan", lazy="select",
    )
    tool_rels: Mapped[list["ProfessionToolRel"]] = relationship(
        "ProfessionToolRel", back_populates="profession",
        cascade="all, delete-orphan", lazy="select",
    )
    study_program_rels: Mapped[list["ProfessionStudyProgramRel"]] = relationship(
        "ProfessionStudyProgramRel", back_populates="profession",
        cascade="all, delete-orphan", lazy="select",
    )

    def __repr__(self) -> str:
        return f"<Profession id={self.id} slug={self.slug}>"
