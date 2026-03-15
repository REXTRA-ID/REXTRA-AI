from sqlalchemy.orm import Session
from app.db.models.kenalidiri_history import KenaliDiriHistory
from datetime import datetime, timezone


class HistoryRepository:
    def get_by_user_id(self, db: Session, user_id):
        """Query history by user_id (UUID), sorted by started_at DESC"""
        try:
            return db.query(KenaliDiriHistory).filter(
                KenaliDiriHistory.user_id == str(user_id)
            ).order_by(KenaliDiriHistory.started_at.desc()).all()
        except Exception:
            # Kalau tabel belum ada / migrasi belum dijalankan
            return []

    def get_by_id(self, db: Session, id: int):
        """Query single history by ID"""
        try:
            return db.query(KenaliDiriHistory).filter(
                KenaliDiriHistory.id == id
            ).first()
        except Exception:
            return None

    def create(
            self,
            db: Session,
            user_id,
            category_id: int,
            detail_session_id: int
    ):
        """Create new history record"""
        history = KenaliDiriHistory(
            user_id=str(user_id),
            test_category_id=category_id,
            detail_session_id=detail_session_id,
            status="ongoing"
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    def update_status(self, db: Session, id: int, status: str):
        """Update status"""
        history = self.get_by_id(db, id)
        if history:
            history.status = status
            db.commit()
            db.refresh(history)
        return history

    def complete(self, db: Session, id: int):
        """Mark as completed"""
        history = self.get_by_id(db, id)
        if history:
            history.status = "completed"
            history.completed_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(history)
        return history
