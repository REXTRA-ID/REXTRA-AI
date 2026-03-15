from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.v1.dependencies.auth import require_active_membership
from app.core.rate_limit import limiter
from app.api.v1.kenali_diri.career_profile.services.result_service import ResultService
from app.api.v1.kenali_diri.career_profile.schemas.result import (
    PersonalityResultResponse,
    FitCheckResultResponse,
    RecommendationResultResponse
)
from app.db.models.user import User

router = APIRouter(
    prefix="/career-profile/result",
    tags=["Career Profile - Result"]
)

@router.get(
    "/personality/{session_token}",
    response_model=PersonalityResultResponse,
    summary="Get RIASEC Personality Result"
)
@limiter.limit("30/minute")
async def get_personality_result(
    request: Request,
    session_token: str,
    current_user: User = Depends(require_active_membership),
    db: Session = Depends(get_db)
):
    """
    Get RIASEC scores and the generated personality description from AI.
    """
    service = ResultService(db)
    return await service.get_personality_result(session_token, current_user)


@router.get(
    "/fit-check/{session_token}",
    response_model=FitCheckResultResponse,
    summary="Get Fit Check Classification Result"
)
@limiter.limit("30/minute")
async def get_fit_check_result(
    request: Request,
    session_token: str,
    current_user: User = Depends(require_active_membership),
    db: Session = Depends(get_db)
):
    """
    Get rule-based classification of Fit Check based on Holland Hexagon match.
    """
    service = ResultService(db)
    return service.get_fit_check_result(session_token, current_user)


@router.get(
    "/recommendation/{session_token}",
    response_model=RecommendationResultResponse,
    summary="Get Final Career Recommendation Narrative"
)
@limiter.limit("30/minute")
async def get_recommendation_result(
    request: Request,
    session_token: str,
    current_user: User = Depends(require_active_membership),
    db: Session = Depends(get_db)
):
    """
    Get the top 2 profession recommendation narratives and Ikigai dimension summary.
    """
    service = ResultService(db)
    return await service.get_recommendation_result(session_token, current_user)
