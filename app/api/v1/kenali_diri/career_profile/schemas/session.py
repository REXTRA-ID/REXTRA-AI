from pydantic import BaseModel, field_validator
from typing import List


class StartRecommendationRequest(BaseModel):
    """
    Request body untuk endpoint POST /career-profile/recommendation/start.

    Validasi persona_type:
      - Hanya menerima: PATHFINDER, BUILDER, ACHIEVER
      - FIT_CHECK tidak ada di sini karena endpoint berbeda
    """
    persona_type: str  # PATHFINDER / BUILDER / ACHIEVER

    @field_validator("persona_type")
    @classmethod
    def validate_persona(cls, v: str) -> str:
        valid = {"PATHFINDER", "BUILDER", "ACHIEVER"}
        if v not in valid:
            raise ValueError(
                f"persona_type '{v}' tidak valid untuk RECOMMENDATION. "
                f"Pilih dari: {sorted(valid)}"
            )
        return v


class StartFitCheckRequest(BaseModel):
    """
    Request body untuk endpoint POST /career-profile/fit-check/start.

    Validasi persona_type:
      - Hanya menerima: BUILDER, ACHIEVER
      - PATHFINDER tidak bisa FIT_CHECK karena belum punya profesi target
    """
    persona_type: str
    target_profession_id: int  # Wajib: ID profesi yang mau dicek kecocokannya

    @field_validator("persona_type")
    @classmethod
    def validate_persona(cls, v: str) -> str:
        valid = {"BUILDER", "ACHIEVER"}
        if v not in valid:
            raise ValueError(
                f"persona_type '{v}' tidak valid untuk FIT_CHECK. "
                f"FIT_CHECK hanya tersedia untuk: {sorted(valid)}"
            )
        return v


class StartSessionResponse(BaseModel):
    """
    Response setelah sesi tes berhasil dibuat.
    Dikirim ke Flutter sebagai konfirmasi + data soal.
    """
    session_token: str
    test_goal: str           # RECOMMENDATION / FIT_CHECK
    status: str              # riasec_ongoing
    question_ids: List[int]  # Urutan 72 ID soal — Flutter harus tampilkan sesuai urutan ini
    total_questions: int     # Selalu 72
    message: str
