from sqlalchemy import Column, BigInteger, String, ForeignKey, TIMESTAMP, Numeric, Boolean
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy.sql import func
from app.db.base import Base

class CareerRecommendation(Base):
    """
    Menyimpan JSON hasil narasi rekomendasi akhir dari Gemini untuk tes IKIGAI.
    Tabel ini adalah hasil akhir dari alur RECOMMENDATION.
    """
    __tablename__ = "career_recommendations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    test_session_id = Column(
        BigInteger,
        ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    recommendations_data = Column(JSONB, nullable=False)
    top_profession1_id = Column(BigInteger, nullable=True)
    top_profession2_id = Column(BigInteger, nullable=True)
    generated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    ai_model_used = Column(String(50), default="gemini-1.5-flash")


class FitCheckResult(Base):
    """
    Menyimpan hasil klasifikasi kecocokan profesi (Fit Check) secara rule-based 
    (berdasarkan Holland Hexagon) untuk tes FIT_CHECK.
    """
    __tablename__ = "fit_check_results"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    test_session_id = Column(
        BigInteger,
        ForeignKey("careerprofile_test_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    profession_id = Column(BigInteger, nullable=False)
    user_riasec_code_id = Column(BigInteger, nullable=False)
    profession_riasec_code_id = Column(BigInteger, nullable=False)
    match_category = Column(
        ENUM('HIGH', 'MEDIUM', 'LOW', name='match_category_enum', create_type=False),
        nullable=False
    )
    rule_type = Column(String(50), nullable=False)
    dominant_letter_same = Column(Boolean, nullable=False)
    is_adjacent_hexagon = Column(Boolean, nullable=False)
    match_score = Column(Numeric(4, 2), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
