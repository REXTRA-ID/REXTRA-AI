"""
app/models/profession_alias.py
------------------------------
Entity: profession_aliases
"""
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.profession import Profession

class ProfessionAlias(Base):
    __tablename__ = "profession_aliases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profession_id: Mapped[int] = mapped_column(ForeignKey("professions.id", ondelete="CASCADE"), nullable=False)
    alias_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    profession: Mapped["Profession"] = relationship("Profession", back_populates="aliases", lazy="select")

    def __repr__(self) -> str:
        return f"<ProfessionAlias id={self.id} name={self.alias_name}>"
