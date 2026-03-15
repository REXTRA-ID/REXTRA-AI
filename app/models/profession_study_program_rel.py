"""
app/models/profession_study_program_rel.py
------------------------------------------
Entity: profession_study_program_rels

Struktur DB aktual (4 columns):
  profession_id    int8  PK, FK → professions.id
  study_program_id int8  PK, FK → study_programs.id
  (2 kolom lain — kemungkinan created_at/updated_at)

PRIMARY KEY: composite (study_program_id, profession_id) — tidak ada kolom `id`

Perubahan: hapus kolom `id`, ganti ke composite PK.
"""
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from app.models.profession import Profession

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ProfessionStudyProgramRel(Base):
    __tablename__ = "profession_study_program_rels"

    profession_id: Mapped[int] = mapped_column(
        ForeignKey("professions.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )
    study_program_id: Mapped[int] = mapped_column(
        ForeignKey("study_programs.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    profession: Mapped["Profession"] = relationship(
        "Profession", back_populates="study_program_rels", lazy="select"
    )

    def __repr__(self) -> str:
        return (
            f"<ProfessionStudyProgramRel profession_id={self.profession_id} "
            f"study_program_id={self.study_program_id}>"
        )