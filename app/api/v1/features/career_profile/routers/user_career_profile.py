# app/api/v1/categories/career_profile/routers/user_career_profile.py
"""
Router untuk manajemen profil karier aktif user.

Endpoints:
  GET  /career-profile/user-profile            → cek profil aktif
  POST /career-profile/user-profile/set-active → set profil baru (tes ke-2+)
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.rate_limit import limiter
from app.api.v1.dependencies.auth import require_active_membership
from app.api.v1.features.career_profile.services.user_career_profile_service import (
    UserCareerProfileService,
)
from app.api.v1.features.career_profile.schemas.user_career_profile import (
    UserCareerProfileResponse,
    SetActiveProfileRequest,
    SetActiveProfileResponse,
)
from app.db.models.user import User

router = APIRouter(
    prefix="/career-profile",
    tags=["Career Profile - User Profile"],
)


@router.get(
    "/user-profile",
    response_model=UserCareerProfileResponse,
    summary="Cek profil karier aktif user",
)
@limiter.limit("60/minute")
async def get_user_career_profile(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership),
):
    """
    Cek apakah user sudah punya profil karier aktif.

    Digunakan oleh Flutter untuk:
    - Tes pertama: `has_active_profile=false` → langsung mulai tes baru
    - Tes berikutnya: `has_active_profile=true` → tampilkan opsi "jadikan profil aktif"
      setelah tes selesai

    Response `has_active_profile=false` jika belum pernah selesai tes RECOMMENDATION.
    """
    svc = UserCareerProfileService(db)
    return svc.get_active_profile(current_user.id)


@router.post(
    "/user-profile/set-active",
    response_model=SetActiveProfileResponse,
    summary="Set sesi RECOMMENDATION tertentu sebagai profil aktif",
)
@limiter.limit("30/minute")
async def set_active_career_profile(
    request: Request,
    body: SetActiveProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership),
):
    """
    Set sesi RECOMMENDATION yang sudah selesai sebagai profil karier aktif user.

    Dipanggil Flutter saat user memilih "Jadikan profil aktif" di layar hasil tes ke-2+.

    Validasi:
    - Sesi harus milik user yang sedang login
    - Status sesi harus `completed`
    - Test goal harus `RECOMMENDATION`

    Profil aktif sebelumnya akan di-non-aktifkan otomatis.
    """
    svc = UserCareerProfileService(db)
    return svc.set_active_profile(current_user.id, body.session_token)
