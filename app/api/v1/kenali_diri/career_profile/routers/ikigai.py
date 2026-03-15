# app/api/v1/categories/career_profile/routers/ikigai.py
"""
Router Ikigai — Career Profile API

Perubahan dari versi sebelumnya:
- Poin 3: Tambah endpoint POST /submit-with-clicks (batch 4 dimensi sekaligus)
- Poin 4: Tambah endpoint GET /dimensions (metadata statis per dimensi, tanpa auth)
- Poin 14: submit_dimension meneruskan selected_profession_ids (List[int]) ke service
- Poin 15: selection_type diteruskan ke service untuk konteks scoring prompt
"""
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union

from app.db.session import get_db
from app.core.rate_limit import limiter
from app.api.v1.dependencies.auth import require_active_membership
from app.api.v1.kenali_diri.career_profile.services.ikigai_service import IkigaiService
from app.api.v1.kenali_diri.career_profile.schemas.ikigai import (
    StartIkigaiRequest,
    IkigaiContentResponse,
    SubmitDimensionRequest,
    DimensionSubmitResponse,
    IkigaiCompletionResponse,
    SubmitWithClicksRequest,        # Poin 3
    IkigaiDimensionsResponse,       # Poin 4
    IkigaiDimensionInfo,            # Poin 4
)
from app.api.v1.kenali_diri.career_profile.prompts.ikigai_prompts import (
    DIMENSION_METADATA,             # Poin 4
)
from app.db.models.user import User

router = APIRouter(
    prefix="/career-profile/ikigai",
    tags=["Career Profile - Ikigai"],
)


# ============================================================
# POIN 4 — GET /dimensions
# Metadata statis 4 dimensi Ikigai untuk Flutter.
# Tidak butuh auth — Flutter pakai untuk render label & helper text soal.
# POIN 15: Response include helper_text_selected & helper_text_not_selected.
# ============================================================

@router.get("/dimensions", response_model=IkigaiDimensionsResponse)
@limiter.limit("60/minute")
async def get_ikigai_dimensions(request: Request):
    """
    Metadata statis 4 dimensi Ikigai.

    Dikembalikan per dimensi:
    - dimension_key, label, label_id
    - question_prompt: pertanyaan utama yang ditampilkan Flutter
    - description: penjelasan tujuan dimensi
    - helper_text_selected: teks bantuan jika user memilih opsi (poin 15)
    - helper_text_not_selected: teks bantuan jika tidak memilih (poin 15)
    - example_text_selected / example_text_not_selected
    - min_chars / max_chars untuk validasi reasoning_text di Flutter

    Tidak membutuhkan auth atau session.
    """
    return IkigaiDimensionsResponse(
        dimensions=[IkigaiDimensionInfo(**d) for d in DIMENSION_METADATA],
        total=len(DIMENSION_METADATA),
    )


@router.post("/start", response_model=IkigaiContentResponse)
@limiter.limit("1000/hour")
async def start_ikigai_session(
    request: Request,
    body: StartIkigaiRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership),
):
    """
    Memulai fase Ikigai.
    - Validasi sesi harus 'riasec_completed'
    - Ubah status sesi ke 'ikigai_ongoing'
    - Generate narasi dimensi (dimension_content) + opsi checkbox (dimension_options) via Gemini
    - Cache konten di Redis selama 2 jam

    Response candidates_with_content kini include dimension_options
    (opsi 1 kalimat per dimensi untuk checkbox di soal Flutter — poin 13).
    """
    service = IkigaiService(db)
    return await service.start_ikigai_session(
        user=current_user,
        session_token=body.session_token,
    )


@router.get("/content/{session_token}", response_model=IkigaiContentResponse)
@limiter.limit("30/minute")
async def get_ikigai_content(
    request: Request,
    session_token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership),
):
    """
    Ambil konten soal Ikigai dari cache Redis atau regenerate jika expired.
    Tidak mengubah status sesi.
    """
    service = IkigaiService(db)
    return await service.get_ikigai_content(
        user=current_user,
        session_token=session_token,
    )


@router.post(
    "/submit-dimension",
    response_model=Union[DimensionSubmitResponse, IkigaiCompletionResponse],
)
@limiter.limit("1000/hour")
async def submit_dimension(
    request: Request,
    body: SubmitDimensionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership),
):
    """
    Submit jawaban untuk satu dimensi Ikigai.
    Endpoint ini dipanggil hingga 4 kali (satu per dimensi).

    POIN 14: selected_profession_ids adalah List[int] (0–2 elemen), bukan single ID.
    POIN 15: selection_type diteruskan ke scoring prompt sebagai konteks.

    Jika ini dimensi ke-4:
      - Trigger AI scoring batch (4 Gemini call paralel)
      - INSERT ikigai_dimension_scores + ikigai_total_scores
      - UPDATE status sesi → completed
      - Return IkigaiCompletionResponse

    Jika bukan dimensi terakhir:
      - Simpan jawaban dan return DimensionSubmitResponse dengan progres.
    """
    try:
        body.validate_consistency()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    service = IkigaiService(db)
    return await service.submit_dimension(
        user=current_user,
        session_token=body.session_token,
        dimension_name=body.dimension_name,
        selected_profession_ids=body.selected_profession_ids,   # POIN 14
        selection_type=body.selection_type,                     # POIN 15
        reasoning_text=body.reasoning_text,
    )


# ============================================================
# POIN 3 — POST /submit-with-clicks
# Batch submit 4 dimensi sekaligus (alternatif dari 4x /submit-dimension).
# ============================================================

@router.post("/submit-with-clicks", response_model=IkigaiCompletionResponse)
@limiter.limit("1000/hour")
async def submit_with_clicks(
    request: Request,
    body: SubmitWithClicksRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership),
):
    """
    Batch submit 4 dimensi sekaligus + data klik eksplisit.

    POIN 14: selected_profession_ids per dimensi adalah List[int] (0–2 elemen).
    POIN 15: selection_type per dimensi diteruskan ke scoring.

    Selalu trigger scoring pipeline (semua 4 dimensi dikirim sekaligus).
    Return IkigaiCompletionResponse.
    """
    try:
        body.validate_all_consistency()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    service = IkigaiService(db)
    return await service.submit_with_clicks(
        user=current_user,
        body=body,
    )


@router.get(
    "/result/{session_token}",
    response_model=IkigaiCompletionResponse,
)
@limiter.limit("30/minute")
async def get_ikigai_result(
    request: Request,
    session_token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_membership),
):
    """
    Ambil hasil final Ikigai yang sudah tersimpan.
    Hanya bisa diakses jika sesi sudah completed.
    """
    service = IkigaiService(db)
    return await service.get_ikigai_result(
        session_token=session_token,
        user=current_user,
    )
