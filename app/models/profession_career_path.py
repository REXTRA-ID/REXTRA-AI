"""
app/models/profession_career_path.py
------------------------------------
Entity: profession_career_paths

Struktur DB aktual (9 columns):
  id               int8         PK
  profession_id    int8         NOT NULL, FK → professions.id
  title            varchar(100) NOT NULL
  experience_range varchar(50)  NOT NULL
  salary_min       int8         NULLABLE
  salary_max       int8         NULLABLE
  sort_order       int8         NOT NULL
  created_at       timestamp    NULLABLE
  updated_at       timestamp    NULLABLE

Perubahan dari versi sebelumnya:
  - `level_name`          → `title`
  - `estimated_salary_min` → `salary_min`
  - `estimated_salary_max` → `salary_max`
  - Tambah kolom `experience_range` (ada di DB, sebelumnya tidak ada di model)
  - `sort_order` tipe int8 (Integer) — tidak berubah
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.profession import Profession

from sqlalchemy import Integer, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ProfessionCareerPath(Base):
    __tablename__ = "profession_career_paths"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    profession_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("professions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    experience_range: Mapped[str] = mapped_column(String(50), nullable=False)
    salary_min: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    sort_order: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    profession: Mapped["Profession"] = relationship(
        "Profession", back_populates="career_paths", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<ProfessionCareerPath id={self.id} title={self.title}>"