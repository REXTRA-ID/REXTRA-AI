from sqlalchemy import Column, BigInteger, String, Text
from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP
from app.db.base import Base

class RIASECQuestion(Base):
    __tablename__ = "riasec_questions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    question_id = Column(String(10), unique=True, nullable=False)
    riasec_type = Column(String(1), nullable=False)
    question_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
