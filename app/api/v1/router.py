# app/api/v1/router.py
"""
Main API v1 Router Aggregator

This module aggregates all API v1 routers including the career profile endpoints.
"""
from fastapi import APIRouter

from app.api.v1.features.career_profile.routers import session, riasec, ikigai, result
from app.api.v1.features.career_profile.routers import user_career_profile
from app.api.v1.features import history_router as history
from app.api.v1.master_data.routers import category

# Create main v1 router
api_v1_router = APIRouter(prefix="/api/v1")

# Include career profile routers
api_v1_router.include_router(
    session.router,
    tags=["Career Profile - Session"]
)

api_v1_router.include_router(
    riasec.router,
    tags=["Career Profile - RIASEC"]
)

api_v1_router.include_router(
    ikigai.router,
    tags=["Career Profile - Ikigai"]
)

api_v1_router.include_router(
    category.router,
    tags=["Categories"]
)

api_v1_router.include_router(
    history.router,
    tags=["History"]
)

api_v1_router.include_router(
    result.router,
    tags=["Career Profile - Result"]
)

api_v1_router.include_router(
    user_career_profile.router,
    tags=["Career Profile - User Profile"]
)

# Include other routers as needed
# api_v1_router.include_router(
#     other_router,
#     prefix="/other",
#     tags=["Other Category"]
# )


# API documentation endpoint
@api_v1_router.get("/", tags=["System"])
async def api_root():
    """
    API root endpoint
    
    Provides overview of available API endpoints.
    """
    return {
        "message": "Welcome to REXTRA-AI Career Profile API v1",
        "documentation": "/docs",
        "openapi_spec": "/openapi.json",
        "available_endpoints": {
            "session": {
                "start_session": "POST /api/v1/career-profile/start",
                "get_session": "GET /api/v1/career-profile/session/{session_token}",
                "get_user_sessions": "GET /api/v1/career-profile/sessions/user/{user_id}",
                "abandon_session": "POST /api/v1/career-profile/session/{session_token}/abandon"
            },
            "riasec": {
                "get_questions": "GET /api/v1/career-profile/riasec/questions",
                "submit_riasec": "POST /api/v1/career-profile/riasec/submit",
                "get_result": "GET /api/v1/career-profile/riasec/result/{session_token}",
                "get_candidates": "GET /api/v1/career-profile/riasec/candidates/{session_token}"
            },
            "ikigai": {
                "get_dimensions": "GET /api/v1/career-profile/ikigai/dimensions",
                "submit_ikigai": "POST /api/v1/career-profile/ikigai/submit",
                "submit_with_clicks": "POST /api/v1/career-profile/ikigai/submit-with-clicks",
                "get_result": "GET /api/v1/career-profile/ikigai/result/{session_token}"
            }
        }
    }