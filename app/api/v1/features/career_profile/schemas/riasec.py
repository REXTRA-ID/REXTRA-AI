from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

class RIASECAnswerItem(BaseModel):
    question_id: int
    question_type: str       # "R", "I", "A", "S", "E", atau "C"
    answer_value: int        # 1 (Sangat Tidak Setuju) - 5 (Sangat Setuju)
    answered_at: datetime    # Waktu user menjawab soal ini (untuk analytics)

    @field_validator("answer_value")
    def validate_answer(cls, v):
        if not (1 <= v <= 5):
            raise ValueError("answer_value harus antara 1 dan 5")
        return v

    @field_validator("question_type")
    def validate_question_type(cls, v):
        if v not in {"R", "I", "A", "S", "E", "C"}:
            raise ValueError(f"question_type tidak valid: {v}")
        return v


class RIASECSubmitRequest(BaseModel):
    session_token: str
    responses: List[RIASECAnswerItem]  # Harus tepat 72 item (12 soal × 6 tipe)

    @field_validator("responses")
    def validate_response_count(cls, v):
        if len(v) != 72:
            raise ValueError(f"Harus ada tepat 72 jawaban (12 per tipe RIASEC), diterima {len(v)}")
        return v


class RIASECScores(BaseModel):
    R: int
    I: int
    A: int
    S: int
    E: int
    C: int


class RIASECCodeInfo(BaseModel):
    riasec_code: str
    riasec_title: str
    riasec_description: Optional[str]
    strengths: List[str]
    challenges: List[str]
    strategies: List[str]
    work_environments: List[str]
    interaction_styles: List[str]


class CandidateProfessionItem(BaseModel):
    profession_id: int
    riasec_code_id: int
    expansion_tier: int          # 1=Exact, 2=Kongruen, 3=Subset, 4=Dominan
    congruence_type: str         # "exact_match", "congruent_permutation", dll
    congruence_score: float      # 0.0-1.0
    display_order: int           # Urutan untuk UI. Top 3-5 yang ditampilkan sebagai opsi Ikigai
    path: Optional[str] = None   # "A" atau "B" — hanya ada jika is_inconsistent_profile=True


class RIASECSubmitResponse(BaseModel):
    session_token: str
    test_goal: str
    status: str                             # "riasec_completed"
    scores: RIASECScores
    classification_type: str               # "single" / "dual" / "triple"
    is_inconsistent_profile: bool
    riasec_code_info: RIASECCodeInfo
    candidates: List[CandidateProfessionItem]
    total_candidates: int
    display_candidates_count: int          # Jumlah profesi yang ditampilkan sebagai opsi UI
    validity_warning: Optional[str] = None # Peringatan jika skor rendah
    next_step: str                          # "ikigai" atau "fit_check_result"
