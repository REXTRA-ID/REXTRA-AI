"""
app/models/tool.py
-------------------
Entity: tools

Struktur DB aktual (4 columns):
  id         int8      PK
  name       varchar   NOT NULL
  created_at timestamp
  updated_at timestamp

Perubahan: kolom `slug` dihapus — tidak ada di DB.
"""
from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Tool(Base):
    __tablename__ = "tools"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"<Tool id={self.id} name={self.name}>"