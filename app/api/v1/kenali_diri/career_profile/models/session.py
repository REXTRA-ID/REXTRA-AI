# app/api/v1/categories/career_profile/models/session.py
from sqlalchemy import Column, BigInteger, Boolean, String, TIMESTAMP, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class CareerProfileTestSession(Base):
    __tablename__ = "careerprofile_test_sessions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_token = Column(String(100), nullable=False, unique=True)

    # Snapshot persona saat tes dibuat (tidak berubah meski user ganti persona)
    persona_type = Column(String(20), nullable=False)   # PATHFINDER / BUILDER / ACHIEVER

    # Tujuan tes
    test_goal = Column(String(20), nullable=False)          # RECOMMENDATION / FIT_CHECK
    target_profession_id = Column(BigInteger, nullable=True) # Hanya untuk FIT_CHECK
    uses_ikigai = Column(Boolean, nullable=False)            # True = RECOMMENDATION, False = FIT_CHECK

    # Status alur
    # Nilai yang valid: riasec_ongoing → riasec_completed → ikigai_ongoing → ikigai_completed → completed
    # Untuk FIT_CHECK: riasec_ongoing → riasec_completed → completed (skip ikigai)
    status = Column(String(30), nullable=False, default="riasec_ongoing")

    # Timestamp — PERBAIKAN: nullable=True, bukan server_default=now()
    started_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    riasec_completed_at = Column(TIMESTAMP(timezone=True), nullable=True)   # Diisi saat RIASEC selesai
    ikigai_completed_at = Column(TIMESTAMP(timezone=True), nullable=True)   # Diisi saat Ikigai selesai
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)          # Diisi saat seluruh tes selesai

    # Versioning untuk keperluan audit
    algorithm_version = Column(String(20), nullable=True, default="1.0")
    question_set_version = Column(String(20), nullable=True, default="1.0")

    __table_args__ = (
        Index("idx_careerprofile_sessions_user_id", "user_id"),
        Index("idx_careerprofile_sessions_token", "session_token"),
        Index("idx_careerprofile_sessions_status", "status"),
    )

    def __repr__(self):
        return f"<CareerProfileTestSession id={self.id} goal={self.test_goal} status={self.status}>"
