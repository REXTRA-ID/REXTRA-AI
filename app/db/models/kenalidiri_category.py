from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    String,
    Text,
    Index
)
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship

class KenaliDiriCategory(Base):
    __tablename__ = "kenalidiri_categories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    category_code = Column(String(50), nullable=False, unique=True)
    category_name = Column(String(255), nullable=False)
    description = Column(Text)

    detail_table_name = Column(String(100), nullable=False)

    is_active = Column(Boolean, nullable=False, server_default="true")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    histories = relationship(
        "KenaliDiriHistory",
        back_populates="test_category"
    )

    __table_args__ = (
        Index("idx_kenalidiri_categories_code", "category_code"),
        Index("idx_kenalidiri_categories_active", "is_active"),
    )

    def __repr__(self):
        return f"<KenalidiriCategory {self.category_code}>"
