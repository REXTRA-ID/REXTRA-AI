"""
app/models/profession_main_category.py
---------------------------------------
Entity  : profession_main_categories
Relasi  : (1) → (N) profession_sub_categories
Aturan  : Hard delete. Tidak ada soft delete / is_active / display_order.

⚠️  Akses DB:
    Tabel sudah ada di PostgreSQL online (103.171.84.248:5433/rextra).
    Model ini HANYA merefleksikan tabel — tidak membuat atau mengubah tabel.
"""

from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.profession_sub_category import ProfessionSubCategory
    from app.models.profession import Profession
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ProfessionMainCategory(Base):
    __tablename__ = "profession_main_categories"

    # ── Kolom ─────────────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # [FIX-3]
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # [FIX-3]

    # ── Relasi ────────────────────────────────────────────────────────────────
    sub_categories: Mapped[list["ProfessionSubCategory"]] = relationship(
        "ProfessionSubCategory",
        back_populates="main_category",
        lazy="select",
    )
    professions: Mapped[list["Profession"]] = relationship(
        "Profession",
        back_populates="main_category",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<ProfessionMainCategory id={self.id} code={self.code}>"
