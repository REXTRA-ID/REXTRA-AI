from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.rate_limit import limiter
from app.api.v1.dependencies.auth import require_active_membership
from app.api.v1.kenali_diri.career_profile.services.riasec_service import RIASECService
from app.api.v1.kenali_diri.career_profile.schemas.riasec import (
    RIASECSubmitRequest,
    RIASECSubmitResponse
)
from app.db.models.user import User

router = APIRouter(prefix="/career-profile/riasec")


@router.post("/submit", response_model=RIASECSubmitResponse)
@limiter.limit("1000/hour")
def submit_riasec(
    request: Request,
    body: RIASECSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership)
):
    """
    Submit 72 jawaban RIASEC sekaligus (12 soal × 6 tipe).
    
    Endpoint ini berlaku untuk RECOMMENDATION maupun FIT_CHECK.
    Perbedaannya hanya di field next_step pada response:
    - RECOMMENDATION → next_step: "ikigai"
    - FIT_CHECK       → next_step: "fit_check_result"
    """
    service = RIASECService(db)
    return service.submit_riasec_test(
        user=current_user,
        session_token=body.session_token,
        responses=body.responses
    )


@router.get("/result/{session_token}", response_model=RIASECSubmitResponse)
@limiter.limit("60/minute")
def get_riasec_result(
    request: Request,
    session_token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership)
):
    """
    Ambil hasil RIASEC yang sudah tersimpan.
    Digunakan Flutter untuk reload halaman hasil tanpa submit ulang.
    """
    service = RIASECService(db)
    return service.get_result(session_token=session_token, user=current_user)
