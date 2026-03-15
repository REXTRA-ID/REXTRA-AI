# app/api/v1/categories/career_profile/services/user_career_profile_service.py
"""
Service untuk manajemen user_career_profiles.

Dipanggil dari:
1. ikigai_service._finalize_ikigai()   — trigger otomatis (tes pertama)
2. Router GET  /user-profile           — cek profil aktif
3. Router POST /user-profile/set-active — set profil baru
"""
from __future__ import annotations
from typing import Optional
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.features.career_profile.models.user_career_profile import UserCareerProfile
from app.api.v1.features.career_profile.models.session import CareerProfileTestSession
from app.api.v1.features.career_profile.models.result import CareerRecommendation
from app.api.v1.features.career_profile.models.riasec import RIASECResult, RIASECCode


class UserCareerProfileService:

    def __init__(self, db: Session):
        self.db = db

    # ──────────────────────────────────────────────────────────────────────────
    # INTERNAL — dipanggil oleh ikigai_service._finalize_ikigai()
    # ──────────────────────────────────────────────────────────────────────────

    def auto_save_if_first(
        self,
        user_id,
        session: CareerProfileTestSession,
        top_profession1_id: Optional[int] = None,
        top_profession2_id: Optional[int] = None,
        riasec_code: Optional[str] = None,
    ) -> Optional[UserCareerProfile]:
        """
        Gunakan SQLAlchemy (Satu Transaksi dengan FastAPI).
        """
        print(f"DEBUG: Menjalankan auto_save_if_first untuk user_id: {user_id}")
        try:
            # 1. Cek keberadaan profil aktif
            existing_active = (
                self.db.query(UserCareerProfile)
                .filter(
                    UserCareerProfile.user_id == user_id,
                    UserCareerProfile.is_active == True,
                )
                .first()
            )

            if existing_active is not None:
                print(f"DEBUG: User sudah punya profil aktif. Skip.")
                return None

            # 2. Buat profil baru
            profile = UserCareerProfile(
                user_id=user_id,
                test_session_id=session.id,
                top_profession1_id=top_profession1_id,
                top_profession2_id=top_profession2_id,
                riasec_code=riasec_code,
                is_active=True,
                activated_at=datetime.now(timezone.utc),
            )
            self.db.add(profile)
            # JANGAN COMMIT DI SINI - Biar caller yang commit (Atomic Transaction)
            print(f"DEBUG: Objek UserCareerProfile ditambahkan ke session untuk user_id: {user_id}")
            return profile
            
        except Exception as e:
            print(f"DEBUG: Gagal menambahkan profil aktif ke session: {str(e)}")
            raise e

    # ──────────────────────────────────────────────────────────────────────────
    # GET /career-profile/user-profile
    # ──────────────────────────────────────────────────────────────────────────

    def get_active_profile(self, user_id) -> dict:
        """Ambil profil karier aktif user. Return has_active_profile=False jika belum ada."""
        profile = (
            self.db.query(UserCareerProfile)
            .filter(
                UserCareerProfile.user_id == user_id,
                UserCareerProfile.is_active == True,
            )
            .order_by(UserCareerProfile.activated_at.desc())
            .first()
        )

        if not profile:
            return {"has_active_profile": False}

        # Ambil session_token dari sesi
        session = self.db.get(CareerProfileTestSession, profile.test_session_id)

        return {
            "has_active_profile":  True,
            "profile_id":          profile.id,
            "test_session_id":     profile.test_session_id,
            "session_token":       session.session_token if session else None,
            "riasec_code":         profile.riasec_code,
            "top_profession1_id":  profile.top_profession1_id,
            "top_profession2_id":  profile.top_profession2_id,
            "activated_at":        profile.activated_at,
        }

    # ──────────────────────────────────────────────────────────────────────────
    # POST /career-profile/user-profile/set-active
    # ──────────────────────────────────────────────────────────────────────────

    def set_active_profile(self, user_id, session_token: str) -> dict:
        """
        Set sesi RECOMMENDATION tertentu sebagai profil aktif user.

        Langkah:
        1. Validasi sesi: harus milik user + status completed + goal RECOMMENDATION
        2. Non-aktifkan semua profil aktif lama
        3. Cari apakah sudah ada baris untuk sesi ini → update, atau insert baru
        4. Return data profil baru
        """
        # Validasi sesi
        session = (
            self.db.query(CareerProfileTestSession)
            .filter(CareerProfileTestSession.session_token == session_token)
            .first()
        )
        if not session or str(session.user_id) != str(user_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Sesi tidak ditemukan")
        if session.test_goal != "RECOMMENDATION":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Sesi bukan tipe RECOMMENDATION")
        if session.status != "completed":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Tes belum selesai")

        # Ambil data profesi top dari career_recommendations
        rec = (
            self.db.query(CareerRecommendation)
            .filter(CareerRecommendation.test_session_id == session.id)
            .first()
        )
        top1_id = rec.top_profession1_id if rec else None
        top2_id = rec.top_profession2_id if rec else None

        # Ambil kode RIASEC
        riasec_result = (
            self.db.query(RIASECResult)
            .filter(RIASECResult.test_session_id == session.id)
            .first()
        )
        riasec_code = None
        if riasec_result:
            code_obj = self.db.get(RIASECCode, riasec_result.riasec_code_id)
            riasec_code = code_obj.riasec_code if code_obj else None

        # Non-aktifkan semua profil aktif lama
        (
            self.db.query(UserCareerProfile)
            .filter(
                UserCareerProfile.user_id == user_id,
                UserCareerProfile.is_active == True,
            )
            .update({"is_active": False}, synchronize_session=False)
        )

        # Cari baris untuk sesi ini atau buat baru
        existing = (
            self.db.query(UserCareerProfile)
            .filter(
                UserCareerProfile.user_id == user_id,
                UserCareerProfile.test_session_id == session.id,
            )
            .first()
        )
        now = datetime.now(timezone.utc)
        if existing:
            existing.is_active          = True
            existing.activated_at       = now
            existing.top_profession1_id = top1_id
            existing.top_profession2_id = top2_id
            existing.riasec_code        = riasec_code
            profile = existing
        else:
            profile = UserCareerProfile(
                user_id=user_id,
                test_session_id=session.id,
                top_profession1_id=top1_id,
                top_profession2_id=top2_id,
                riasec_code=riasec_code,
                is_active=True,
                activated_at=now,
            )
            self.db.add(profile)

        self.db.commit()
        self.db.refresh(profile)

        return {
            "success":            True,
            "profile_id":         profile.id,
            "test_session_id":    profile.test_session_id,
            "session_token":      session_token,
            "riasec_code":        riasec_code,
            "top_profession1_id": top1_id,
            "top_profession2_id": top2_id,
            "message":            "Profil karier aktif berhasil diperbarui.",
        }
