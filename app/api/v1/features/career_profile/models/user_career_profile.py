# app/api/v1/categories/career_profile/models/user_career_profile.py
"""
Model untuk tabel user_career_profiles.

Menyimpan profil karier aktif user — hasil tes RECOMMENDATION yang dipilih
sebagai "profil utama" untuk ditampilkan di dashboard dan digunakan sebagai
referensi FIT_CHECK.

Tes RECOMMENDATION pertama → auto-insert.
Tes RECOMMENDATION berikutnya → user bisa set manual via POST /user-profile/set-active.
"""
from sqlalchemy import Column, BigInteger, Boolean, ForeignKey, TIMESTAMP, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class UserCareerProfile(Base):
    __tablename__ = "user_career_profiles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # User yang punya profil
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Sesi tes RECOMMENDATION yang jadi sumber profil ini
    test_session_id = Column(
        BigInteger,
        ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Profesi top 1 dan 2 dari hasil tes (denormalisasi untuk query cepat)
    top_profession1_id = Column(BigInteger, nullable=True)
    top_profession2_id = Column(BigInteger, nullable=True)

    # Kode RIASEC user saat tes (misal: "RI", "RIA", "SEC")
    riasec_code = Column(String(6), nullable=True)

    # Apakah ini profil yang sedang aktif
    is_active = Column(Boolean, nullable=False, default=True)

    # Timestamp
    created_at  = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    activated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=True)

    __table_args__ = (
        Index("idx_user_career_profiles_user_id", "user_id"),
        Index("idx_user_career_profiles_session_id", "test_session_id"),
        Index("idx_user_career_profiles_user_active", "user_id", "is_active"),
    )

    def __repr__(self):
        return (
            f"<UserCareerProfile user={self.user_id} "
            f"session={self.test_session_id} active={self.is_active}>"
        )
