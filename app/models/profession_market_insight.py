"""
app/models/profession_market_insight.py
---------------------------------------
Entity: profession_market_insights
"""
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.profession import Profession

class ProfessionMarketInsight(Base):
    __tablename__ = "profession_market_insights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profession_id: Mapped[int] = mapped_column(ForeignKey("professions.id", ondelete="CASCADE"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    profession: Mapped["Profession"] = relationship("Profession", back_populates="market_insights", lazy="select")

    def __repr__(self) -> str:
        return f"<ProfessionMarketInsight id={self.id} profession_id={self.profession_id}>"
