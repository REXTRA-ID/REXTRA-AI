from sqlalchemy.orm import Session
from app.api.v1.features.career_profile.models.riasec import (
    RIASECCode, RIASECQuestionSet, RIASECResponse, RIASECResult
)

class RIASECRepository:
    def __init__(self, db: Session = None):
        """
        Mendukung dua pola penggunaan:
        1. Constructor injection: repo = RIASECRepository(db)  — dipakai profession_expansion.py
        2. Tanpa db: repo = RIASECRepository(); repo.get_code_by_id(db, id) — pola lama
        """
        self.db = db

    def get_riasec_code_by_string(self, code: str):
        """
        Convenience method: cari RIASECCode berdasarkan string kode (e.g. 'RIA', 'RI').
        Digunakan oleh profession_expansion.py.
        Menggunakan self.db yang di-inject via constructor.
        Raise HTTPException 404 jika tidak ditemukan.
        """
        from fastapi import HTTPException, status
        if not self.db:
            raise RuntimeError("RIASECRepository tidak punya db session — gunakan constructor injection.")
        code_obj = self.db.query(RIASECCode).filter_by(riasec_code=code).first()
        if not code_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RIASEC code '{code}' tidak ditemukan di database."
            )
        return code_obj

    def get_active_question_set(self, db: Session):
        """Get active question set (72 questions)"""
        question_set = db.query(RIASECQuestionSet).filter_by(is_active=True).first()
        if question_set:
            return question_set.questions_data
        return []
    
    def get_code_by_id(self, db: Session, code_id: int):
        """Get RIASEC code by ID"""
        return db.query(RIASECCode).filter_by(id=code_id).first()
    
    def get_code_by_code(self, db: Session, code: str):
        """Get RIASEC code by code string (e.g. 'RIA')"""
        return db.query(RIASECCode).filter_by(riasec_code=code).first()
    
    def save_responses(self, db: Session, session_id: int, responses: dict):
        """Save RIASEC responses"""
        response = RIASECResponse(
            test_session_id=session_id,
            responses_data=responses
        )
        db.add(response)
        db.commit()
        db.refresh(response)
        return response
    
    def save_result(
        self,
        db: Session,
        session_id: int,
        scores: dict,
        code_id: int,
        code_type: str
    ):
        """Save RIASEC result"""
        result = RIASECResult(
            test_session_id=session_id,
            score_r=scores.get("R", 0),
            score_i=scores.get("I", 0),
            score_a=scores.get("A", 0),
            score_s=scores.get("S", 0),
            score_e=scores.get("E", 0),
            score_c=scores.get("C", 0),
            riasec_code_id=code_id,
            riasec_code_type=code_type
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    
    def get_result_by_session(self, db: Session, session_id: int):
        """Get RIASEC result by session ID"""
        return db.query(RIASECResult).filter_by(test_session_id=session_id).first()
