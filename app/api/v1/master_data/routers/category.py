from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.v1.general.repositories.category_repo import CategoryRepository
from app.api.v1.general.schemas import CategoryResponse
from app.core.rate_limit import limiter
from fastapi import Request

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryResponse])
@limiter.limit("100/minute")
async def list_categories(
    request: Request,
    db: Session = Depends(get_db)
):
    """List semua kategori tes yang aktif"""
    repo = CategoryRepository()
    categories = repo.get_all_active(db)
    return categories
