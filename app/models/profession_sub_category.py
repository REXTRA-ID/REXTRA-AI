"""
app/models/profession_sub_category.py
---------------------------------------
Entity  : profession_sub_categories
Relasi  :
    (N) → (1) profession_main_categories  via main_category_id
    (1) → (N) professions

Constraint DB (sudah ada di tabel):
    UNIQUE (main_category_id, code)
    UNIQUE (main_category_id, name)

⚠️  Akses DB:
    Tabel sudah ada di PostgreSQL online (103.171.84.248:5433/rextra).
    Model ini HANYA merefleksikan tabel — tidak membuat atau mengubah tabel.
"""

from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.profession_main_category import ProfessionMainCategory
    from app.models.profession import Profession
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ProfessionSubCategory(Base):
    __tablename__ = "profession_sub_categories"

    # ── Kolom ─────────────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    main_category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profession_main_categories.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # [FIX-3]
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # [FIX-3]

    # ── Relasi ────────────────────────────────────────────────────────────────
    main_category: Mapped["ProfessionMainCategory"] = relationship(
        "ProfessionMainCategory",
        back_populates="sub_categories",
        lazy="select",
    )
    professions: Mapped[list["Profession"]] = relationship(
        "Profession",
        back_populates="sub_category",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<ProfessionSubCategory id={self.id} code={self.code}>"
