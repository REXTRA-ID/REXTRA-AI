from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    CheckConstraint
)
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship


from sqlalchemy.dialects.postgresql import UUID


class KenaliDiriHistory(Base):
    __tablename__ = "kenalidiri_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id = Column(UUID(as_uuid=True), nullable=False)

    test_category_id = Column(
        BigInteger,
        ForeignKey(
            "kenalidiri_categories.id",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    detail_session_id = Column(BigInteger, nullable=False)

    status = Column(
        String(20),
        CheckConstraint(
            "status IN ('ongoing', 'completed', 'abandoned')",
            name="chk_kenalidiri_history_status"
        ),
        nullable=False
    )

    test_category = relationship(
        "KenaliDiriCategory",
        back_populates="histories"
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    completed_at = Column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_kenalidiri_history_user_id", "user_id"),
        Index("idx_kenalidiri_history_category_id", "test_category_id"),
        Index("idx_kenalidiri_history_status", "status"),
        Index("idx_kenalidiri_history_started_at", "started_at"),
    )

    def __repr__(self):
        return f"<KenalidiriHistory user_id={self.user_id} status={self.status}>"
