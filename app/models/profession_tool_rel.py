"""
app/models/profession_tool_rel.py
----------------------------------
Entity: profession_tool_rels

Struktur DB aktual (5 columns):
  profession_id  int8      PK, FK → professions.id
  tool_id        int8      PK, FK → tools.id
  created_at     timestamp
  updated_at     timestamp
  (+ 1 kolom lain — kemungkinan tool_type atau priority, belum dikonfirmasi)

PRIMARY KEY: composite (profession_id, tool_id) — tidak ada kolom `id`

Perubahan: hapus kolom `id`, ganti ke composite PK.
"""
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from app.models.profession import Profession
    from app.models.tool import Tool

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ProfessionToolRel(Base):
    __tablename__ = "profession_tool_rels"

    profession_id: Mapped[int] = mapped_column(
        ForeignKey("professions.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )
    tool_id: Mapped[int] = mapped_column(
        ForeignKey("tools.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    profession: Mapped["Profession"] = relationship(
        "Profession", back_populates="tool_rels", lazy="select"
    )
    tool: Mapped["Tool"] = relationship("Tool", lazy="joined")

    def __repr__(self) -> str:
        return f"<ProfessionToolRel profession_id={self.profession_id} tool_id={self.tool_id}>"