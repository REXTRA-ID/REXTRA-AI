from pydantic import BaseModel
from typing import Optional, List


# ── Shared building blocks ────────────────────────────────────────────────────

class TopTypeItem(BaseModel):
    """Satu huruf RIASEC beserta nama tipenya. Digunakan di PersonalityResultResponse."""
    letter: str   # "R", "I", "A", "S", "E", atau "C"
    name: str     # "Realistic", "Investigative", dst.


class RIASECSummary(BaseModel):
    """Ringkasan profil RIASEC. Digunakan di FitCheckResultResponse dan RecommendationResultResponse."""
    riasec_code:           str
    riasec_title:          str
    top_types:             List[str]
    total_candidates_found: Optional[int] = None  # hanya untuk RECOMMENDATION


# ── Personality Tab (shared endpoint) ────────────────────────────────────────

class PersonalityResultResponse(BaseModel):
    """
    Response GET /result/personality/{session_token}
    Shared endpoint — bisa dipanggil dari halaman RECOMMENDATION maupun FIT_CHECK.
    """
    session_token:      str
    riasec_code:        str
    riasec_title:       str
    top_types:          List[TopTypeItem]
    about_code:         str
    strengths:          List[str]
    challenges:         List[str]
    strategies:         List[str]
    interaction_styles: List[str]
    work_environments:  List[str]


# ── FIT CHECK ─────────────────────────────────────────────────────────────────

class FitCheckExplanation(BaseModel):
    """Penjelasan dinamis rule-based hasil Fit Check."""
    meaning:       str
    reason_points: List[str]
    implication:   str
    next_steps:    List[str]
    cta_primary:   str
    cta_secondary: Optional[str]
    match_label:   str
    match_stars:   int


class TargetProfession(BaseModel):
    """Profesi yang dicek dalam sesi FIT_CHECK."""
    profession_id: int
    name:          str
    riasec_code:   str
    riasec_title:  str


class FitCheckResultItem(BaseModel):
    """Wrapper item hasil Fit Check."""
    match_category:      str    # "HIGH" / "MEDIUM" / "LOW"
    match_label:         str    # "Kecocokan Tinggi" / "Kecocokan Sedang" / "Kecocokan Rendah"
    match_stars:         int    # 3 / 2 / 1
    rule_type:           str
    dominant_letter_same: bool
    is_adjacent_hexagon: bool
    match_score:         Optional[float]
    explanation:         FitCheckExplanation


class FitCheckResultResponse(BaseModel):
    """Response GET /result/fit-check/{session_token}"""
    session_token:    str
    user_first_name:  str
    test_completed_at: Optional[str]
    user_riasec:      RIASECSummary
    target_profession: TargetProfession
    fit_check_result: FitCheckResultItem
    points_awarded:   Optional[str] = None
    TODO_points: Optional[str] = (
        "Implementasi poin Rextra belum aktif. Tambahkan setelah tabel points dikonfirmasi."
    )


# ── RECOMMENDATION ────────────────────────────────────────────────────────────

class ScoreBreakdown(BaseModel):
    """Breakdown skor Ikigai per dimensi untuk satu profesi."""
    total_score:              Optional[float] = 0.0
    intrinsic_score:          Optional[float] = 0.0
    extrinsic_score:          Optional[float] = 0.0
    score_what_you_love:      Optional[float] = 0.0
    score_what_you_are_good_at: Optional[float] = 0.0
    score_what_the_world_needs: Optional[float] = 0.0
    score_what_you_can_be_paid_for: Optional[float] = 0.0


class RIASECAlignment(BaseModel):
    """Informasi keselarasan RIASEC antara user dan profesi yang direkomendasikan."""
    user_code:        Optional[str] = ""
    profession_code:  Optional[str] = ""
    congruence_type:  Optional[str] = ""
    congruence_score: Optional[float] = 0.0


class RecommendedProfession(BaseModel):
    """Satu profesi yang direkomendasikan beserta narasi dan skor."""
    rank:             int
    profession_id:    int
    profession_name:  str
    match_percentage: float
    match_reasoning:  Optional[str] = ""
    riasec_alignment: Optional[RIASECAlignment] = None
    score_breakdown:  Optional[ScoreBreakdown] = None


class CandidateProfessionName(BaseModel):
    """Pasangan ID+nama untuk satu profesi kandidat — hanya untuk list display."""
    profession_id: int
    name:          str


class IkigaiProfileSummary(BaseModel):
    """Narasi ringkasan 4 dimensi Ikigai dari Gemini."""
    what_you_love:            Optional[str] = ""
    what_you_are_good_at:     Optional[str] = ""
    what_the_world_needs:     Optional[str] = ""
    what_you_can_be_paid_for: Optional[str] = ""


class RIASECScores(BaseModel):
    """Skor mentah per tipe RIASEC (range 12–60)."""
    R: int = 0
    I: int = 0
    A: int = 0
    S: int = 0
    E: int = 0
    C: int = 0


class RIASECProfile(BaseModel):
    """Profil kepribadian lengkap dari tabel riasec_codes — untuk Tab Kepribadian UI."""
    riasec_code:        str
    riasec_title:       str
    riasec_description: Optional[str] = ""
    strengths:          List[str] = []
    challenges:         List[str] = []
    strategies:         List[str] = []
    interaction_styles: List[str] = []
    work_environments:  List[str] = []


class CandidateProfessionFull(BaseModel):
    """Kandidat profesi lengkap dengan metadata kongruensi."""
    profession_id:        int
    name:                 str
    congruence_type:      Optional[str] = ""
    expansion_tier:       Optional[int] = None
    is_display_candidate: bool = True


class RecommendationResultResponse(BaseModel):
    """Response GET /result/recommendation/{session_token}"""
    """Response GET /result/recommendation/{session_token}
    
    Berisi semua data yang dibutuhkan halaman Hasil Tes:
    - Tab Rekomendasi: riasec_summary + kandidat + ikigai + top 2 rekomendasi
    - Tab Kepribadian: riasec_profile (strengths, challenges, strategies, dll)
    """
    session_token:             str
    user_first_name:           str
    test_completed_at:         Optional[str]

    # ── Tab Rekomendasi ──────────────────────────────────────────
    # 3.2 Bar chart RIASEC
    riasec_summary:            RIASECSummary
    riasec_scores_raw:         Optional[RIASECScores] = None

    # 3.3 Kandidat profesi (identik + kongruen)
    candidate_profession_names: List[CandidateProfessionName]     # backward compat
    display_candidates:         List[CandidateProfessionFull] = [] # opsi soal (is_display=True)
    congruent_candidates:       List[CandidateProfessionFull] = [] # backup scoring

    # 3.4 Profil Ikigai per dimensi
    ikigai_profile_summary:    Optional[IkigaiProfileSummary] = None

    # 3.5 Top 2 rekomendasi (nama + % + reasoning 2 kalimat)
    recommended_professions:   List[RecommendedProfession]

    # ── Tab Kepribadian ──────────────────────────────────────────
    # Strengths, Challenges, Strategies, Interaction, Work Env
    riasec_profile:            Optional[RIASECProfile] = None

    # ── Reward / gamification ────────────────────────────────────
    points_awarded:            Optional[str] = None
    test_duration_minutes:     Optional[int] = None
