from sqlalchemy import Column, BigInteger, Boolean, String, Integer, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class IkigaiResponse(Base):
    """
    Menyimpan jawaban user untuk 4 dimensi Ikigai.
    Row di-INSERT saat user mulai Ikigai (kosong/placeholder).
    Diisi bertahap per dimensi via UPDATE.
    One-to-one dengan careerprofile_test_sessions.
    """
    __tablename__ = "ikigai_responses"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    test_session_id = Column(
        BigInteger,
        ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    # Format per kolom dimensi (identik):
    # {
    #   "selected_profession_id": int | null,
    #   "selection_type": "selected" | "not_selected",
    #   "reasoning_text": str,
    #   "answered_at": "ISO8601"
    # }
    # NULL saat baru di-INSERT, diisi via UPDATE per dimensi
    dimension_1_love        = Column(JSONB, nullable=True, name="dimension1_love")
    dimension_2_good_at     = Column(JSONB, nullable=True, name="dimension2_good_at")
    dimension_3_world_needs = Column(JSONB, nullable=True, name="dimension3_world_needs")
    dimension_4_paid_for    = Column(JSONB, nullable=True, name="dimension4_paid_for")

    completed    = Column(Boolean, nullable=False, default=False)
    created_at   = Column(TIMESTAMP(timezone=True), server_default=func.now())
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)


class IkigaiDimensionScores(Base):
    """
    Skor per dimensi untuk semua kandidat profesi.
    INSERT sekali setelah 4 dimensi selesai dan AI scoring batch selesai.
    Immutable — tidak pernah di-UPDATE.
    Data intermediate — dapat dihapus setelah 6–12 bulan untuk menghemat storage.
    One-to-one dengan careerprofile_test_sessions.
    """
    __tablename__ = "ikigai_dimension_scores"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    test_session_id = Column(
        BigInteger,
        ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    scores_data = Column(JSONB, nullable=False)
    calculated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    ai_model_used = Column(String(50), default="gemini-1.5-flash")
    total_api_calls = Column(Integer, default=4)

    __table_args__ = (
        CheckConstraint("total_api_calls BETWEEN 1 AND 20", name="chk_valid_api_calls"),
    )


class IkigaiTotalScores(Base):
    """
    Skor total agregasi dari 4 dimensi untuk semua kandidat profesi.
    INSERT sekali setelah agregasi selesai.
    Immutable dan PERMANEN — tidak pernah dihapus (bagian dari riwayat user).
    One-to-one dengan careerprofile_test_sessions.
    """
    __tablename__ = "ikigai_total_scores"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    test_session_id = Column(
        BigInteger,
        ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    scores_data = Column(JSONB, nullable=False)
    top_profession_1_id = Column(BigInteger, nullable=True, name="top_profession1_id")
    top_profession_2_id = Column(BigInteger, nullable=True, name="top_profession2_id")
    calculated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "top_profession_1_id IS NULL OR top_profession_2_id IS NULL OR "
            "top_profession_1_id != top_profession_2_id",
            name="chk_different_top_professions"
        ),
    )
