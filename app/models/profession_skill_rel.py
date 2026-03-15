"""
app/models/profession_skill_rel.py
----------------------------------
Entity: profession_skill_rels

Struktur DB aktual:
  profession_id  int8        NOT NULL
  skill_id       int8        NOT NULL
  skill_type     varchar(20) NOT NULL
  priority       varchar(20) NOT NULL
  created_at     timestamp   NULLABLE
  updated_at     timestamp   NULLABLE
  PRIMARY KEY (profession_id, skill_id)  — composite, tidak ada kolom id

Perubahan dari versi sebelumnya:
- Hapus kolom `id` (tidak ada di DB)
- Tambah kolom `skill_type` dan `priority` (ada di DB, dibutuhkan untuk filter)
- Ganti primary_key ke composite (profession_id, skill_id)
"""
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from app.models.profession import Profession
    from app.models.skill import Skill

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

VALID_SKILL_TYPES = {"hard", "soft", "other"}
VALID_PRIORITIES  = {"required", "preferred", "optional"}


class ProfessionSkillRel(Base):
    __tablename__ = "profession_skill_rels"

    profession_id: Mapped[int] = mapped_column(
        ForeignKey("professions.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )
    skill_type: Mapped[str] = mapped_column(String(20), nullable=False)
    priority:   Mapped[str] = mapped_column(String(20), nullable=False)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    profession: Mapped["Profession"] = relationship(
        "Profession", back_populates="skill_rels", lazy="select"
    )
    skill: Mapped["Skill"] = relationship("Skill", lazy="joined")

    def __repr__(self) -> str:
        return (
            f"<ProfessionSkillRel profession_id={self.profession_id} "
            f"skill_id={self.skill_id} type={self.skill_type}>"
        )