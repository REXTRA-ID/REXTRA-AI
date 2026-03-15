# app/api/v1/categories/career_profile/repositories/session_repo.py
import uuid
from sqlalchemy.orm import Session
from app.api.v1.kenali_diri.career_profile.models.session import CareerProfileTestSession
from datetime import datetime

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: uuid.UUID):
        """Create new test session, return (session, token)"""
        session_token = str(uuid.uuid4())

        new_session = CareerProfileTestSession(
            user_id=user_id,
            status="riasec_pending",
            session_token=session_token,
            started_at=datetime.now()
        )
        self.db.add(new_session)
        self.db.commit()
        self.db.refresh(new_session)

        # In real implementation, might store token separately or use session_id as token
        return new_session

    def get_by_id(self, session_id: int):
        return self.db.query(CareerProfileTestSession).filter(
            CareerProfileTestSession.id == session_id
        ).first()
    
    def get_by_token(self, db: Session, token: str):
        return db.query(CareerProfileTestSession).filter(
            CareerProfileTestSession.session_token == token
        ).first()

    def get_session_by_token(self, token: str):
        """Get session by token"""
        return self.db.query(CareerProfileTestSession).filter(
            CareerProfileTestSession.session_token == token
        ).first()

    def update_session_status(self, session_id: int, status: str, timestamp_field: str = None):
        """Generic method to update session status and an optional timestamp field"""
        session = self.get_by_id(session_id)
        if session:
            session.status = status
            if timestamp_field and hasattr(session, timestamp_field):
                setattr(session, timestamp_field, datetime.now())
            self.db.commit()
            self.db.refresh(session)
        return session

    def mark_riasec_completed(self, session_id: int):
        """Mark RIASEC as completed"""
        return self.update_session_status(session_id, "ikigai_pending", "riasec_completed_at")

    def mark_ikigai_completed(self, session_id: int):
        """Mark Ikigai as completed"""
        session = self.get_by_id(session_id)
        if session:
            # session.ikigai_completed = True
            session.ikigai_completed_at = datetime.now()
            session.status = "completed"
            session.completed_at = datetime.now()
            self.db.commit()
            self.db.refresh(session)
        return session
