# app/api/v1/categories/career_profile/schemas/user_career_profile.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCareerProfileResponse(BaseModel):
    """Response GET /career-profile/user-profile"""
    has_active_profile: bool

    # Null jika belum punya profil aktif
    profile_id:         Optional[int]    = None
    test_session_id:    Optional[int]    = None
    session_token:      Optional[str]    = None
    riasec_code:        Optional[str]    = None
    top_profession1_id: Optional[int]    = None
    top_profession2_id: Optional[int]    = None
    activated_at:       Optional[datetime] = None

    class Config:
        from_attributes = True


class SetActiveProfileRequest(BaseModel):
    """Body POST /career-profile/user-profile/set-active"""
    session_token: str   # token sesi RECOMMENDATION yang ingin dijadikan profil aktif


class SetActiveProfileResponse(BaseModel):
    """Response POST /career-profile/user-profile/set-active"""
    success:            bool
    profile_id:         int
    test_session_id:    int
    session_token:      str
    riasec_code:        Optional[str] = None
    top_profession1_id: Optional[int] = None
    top_profession2_id: Optional[int] = None
    message:            str
