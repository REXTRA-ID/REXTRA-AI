from sqlalchemy import (
    Column, BigInteger, String, Boolean, Integer,
    ForeignKey, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP
from app.db.base import Base


class RIASECCode(Base):
    """Master data 156 kode RIASEC (6 single + 30 dual + 120 triple). Di-seed via scripts."""
    __tablename__ = "riasec_codes"

    id = Column(BigInteger, primary_key=True)
    riasec_code = Column(String(3), unique=True, nullable=False)
    riasec_title = Column(String(255), nullable=False)
    riasec_description = Column(String, nullable=True)
    strengths = Column(JSONB, server_default="'[]'")
    challenges = Column(JSONB, server_default="'[]'")
    strategies = Column(JSONB, server_default="'[]'")
    work_environments = Column(JSONB, server_default="'[]'")
    interaction_styles = Column(JSONB, server_default="'[]'")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class RIASECQuestionSet(Base):
    """
    Menyimpan urutan 12 ID soal yang di-generate untuk satu sesi.
    PERBAIKAN: kolom ini hanya berisi question_ids (JSONB array), bukan skor.
    Skor ada di riasec_results, bukan di sini.
    """
    __tablename__ = "riasec_question_sets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    test_session_id = Column(
        BigInteger,
        ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True   # One-to-one dengan session
    )
    # Array 72 integer, contoh: [15, 23, 8, 45, 67, 2, 38, 51, 12, 60, 19, 44, ...]
    # (72 soal total = 12 soal × 6 tipe, diacak urutannya — bukan dikelompokkan per tipe)
    # Urutan array = urutan tampil soal ke user
    question_ids = Column(JSONB, nullable=False)
    generated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class RIASECResponse(Base):
    """
    Menyimpan semua 72 jawaban user dalam satu baris JSONB.
    INSERT sekali saat user submit, tidak ada update bertahap.
    One-to-one dengan session.
    """
    __tablename__ = "riasec_responses"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    test_session_id = Column(
        BigInteger,
        ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True   # Satu baris per sesi, tidak boleh double insert
    )
    # Format: {"responses": [...72 items...], "total_questions": 72, "completed": true, "submitted_at": "..."}
    responses_data = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class RIASECResult(Base):
    """
    Menyimpan hasil akhir klasifikasi RIASEC.
    One-to-one dengan session.
    """
    __tablename__ = "riasec_results"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    test_session_id = Column(
        BigInteger,
        ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    # Skor mentah per tipe (range 12-60: 12 soal × nilai 1-5)
    score_r = Column(Integer, nullable=False)
    score_i = Column(Integer, nullable=False)
    score_a = Column(Integer, nullable=False)
    score_s = Column(Integer, nullable=False)
    score_e = Column(Integer, nullable=False)
    score_c = Column(Integer, nullable=False)

    # Hasil klasifikasi
    riasec_code_id = Column(
        BigInteger,
        ForeignKey("riasec_codes.id", ondelete="RESTRICT"),
        nullable=False
    )
    riasec_code_type = Column(String(20), nullable=False)  # "single" / "dual" / "triple"
    is_inconsistent_profile = Column(Boolean, default=False, nullable=False)

    # CATATAN: kolom scores_data dan riasec_code TIDAK ADA di DB production.
    # DB mengikuti Golang entity yang tidak punya kolom ini.
    # Jangan tambahkan kembali tanpa migrasi DB terlebih dahulu.

    calculated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationship to RIASECCode for convenient access
    riasec_code_obj = relationship(
        "RIASECCode",
        foreign_keys=[riasec_code_id],
        lazy="select"
    )

    __table_args__ = (
        CheckConstraint(
            "riasec_code_type IN ('single', 'dual', 'triple')",
            name="chk_riasec_results_classification_type"
        ),
        Index("idx_riasec_results_session", "test_session_id"),
    )
