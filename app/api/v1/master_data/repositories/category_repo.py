from sqlalchemy.orm import Session
from app.db.models import KenaliDiriCategory

class CategoryRepository:
    def get_all_active(self, db: Session):
        """Query semua kategori aktif"""
        return db.query(KenaliDiriCategory).filter(
            KenaliDiriCategory.is_active == True
        ).all()

    def get_by_code(self, db: Session, code: str):
        """Query kategori by code"""
        return db.query(KenaliDiriCategory).filter(
            KenaliDiriCategory.category_code == code
        ).first()

    def get_by_id(self, db: Session, id: int):
        """Query kategori by ID"""
        return db.query(KenaliDiriCategory).filter(
            KenaliDiriCategory.id == id
        ).first()
