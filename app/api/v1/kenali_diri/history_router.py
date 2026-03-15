from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.v1.general.repositories.history_repo import HistoryRepository
from app.api.v1.general.schemas.history import HistoryResponse
from app.core.rate_limit import limiter

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/", response_model=list[HistoryResponse])
@limiter.limit("30/minute")
async def list_history(
        request: Request,
        user_id: int = Query(..., description="User ID"),
        db: Session = Depends(get_db)
):
    """List history tes untuk user tertentu"""
    repo = HistoryRepository()
    history = repo.get_by_user_id(db, user_id)
    return history


@router.get("/{history_id}", response_model=HistoryResponse)
@limiter.limit("30/minute")
async def get_history_detail(
        request: Request,
        history_id: int,
        db: Session = Depends(get_db)
):
    """Get detail single history"""
    repo = HistoryRepository()
    history = repo.get_by_id(db, history_id)

    if not history:
        raise HTTPException(
            status_code=404,
            detail="History not found"
        )

    return history
