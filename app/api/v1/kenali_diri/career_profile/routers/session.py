from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.rate_limit import limiter
from app.api.v1.dependencies.auth import require_active_membership
from app.api.v1.kenali_diri.career_profile.services.session_service import SessionService
from app.api.v1.kenali_diri.career_profile.schemas.session import (
    StartRecommendationRequest,
    StartFitCheckRequest,
    StartSessionResponse
)
from app.db.models.user import User

router = APIRouter(prefix="/career-profile")


@router.post("/recommendation/start", response_model=StartSessionResponse)
@limiter.limit("1000/hour")
def start_recommendation(
    request: Request,
    body: StartRecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership)
):
    """
    Mulai tes Profil Karier — tujuan REKOMENDASI PROFESI.
    Alur lengkap: RIASEC → Ikigai → 2 rekomendasi profesi.
    Biaya: 3 token dipotong di awal.
    
    Dipanggil Flutter untuk semua persona, tapi umumnya PATHFINDER.
    """
    service = SessionService(db)
    return service.start_session(
        user=current_user,
        persona_type=body.persona_type,
        test_goal="RECOMMENDATION",
        uses_ikigai=True,
        target_profession_id=None
    )


@router.post("/fit-check/start", response_model=StartSessionResponse)
@limiter.limit("1000/hour")
def start_fit_check(
    request: Request,
    body: StartFitCheckRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership)
):
    """
    Mulai tes Profil Karier — tujuan CEK KECOCOKAN PROFESI TARGET.
    Alur: RIASEC saja (kode RIASEC user disandingkan kode RIASEC profesi target).
    Biaya: Gratis saat ini.
    
    CATATAN — PERLU DIROMBAK KE DEPAN:
    Saat ini FIT_CHECK tidak ada pembatasan akses sama sekali.
    Jika ke depan ada kuota (misal 3x/bulan) atau berbayar token,
    tambahkan dependency check_fit_check_quota() dari token.py di sini.
    Lihat komentar di app/api/v1/dependencies/token.py untuk panduan implementasi.
    """
    service = SessionService(db)
    return service.start_session(
        user=current_user,
        persona_type=body.persona_type,
        test_goal="FIT_CHECK",
        uses_ikigai=False,
        target_profession_id=body.target_profession_id
    )
