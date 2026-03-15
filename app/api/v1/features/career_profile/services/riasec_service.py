# app/api/v1/categories/career_profile/services/riasec_service.py
"""
RIASEC Service — Ditulis Ulang

Mencakup:
1. Kalkulasi skor mentah (raw sum, bukan rata-rata)
2. Klasifikasi kode RIASEC LENGKAP (semua kondisi, bridge table, tie-breaker)
3. Validasi profil (low overall, severe low, invalid)
4. Lookup detail kode dari database
5. Ekspansi kandidat profesi (4-tier + Split-Path untuk profil inkonsisten)
6. Penyimpanan ke semua tabel
"""
from typing import Dict, List, Tuple, Optional, Any, Set
from itertools import permutations, combinations
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.api.v1.features.career_profile.models.session import CareerProfileTestSession
from app.api.v1.features.career_profile.models.riasec import (
    RIASECQuestionSet, RIASECResponse, RIASECResult, RIASECCode
)
from app.api.v1.features.career_profile.models.ikigai import IkigaiCandidateProfession
from app.api.v1.features.career_profile.repositories.profession_repo import ProfessionRepository
from app.api.v1.features.career_profile.schemas.riasec import RIASECAnswerItem
from app.db.models.user import User


# ============================================================
# KONSTANTA HEKSAGON HOLLAND
# ============================================================

# Pasangan opposite (berseberangan di heksagon)
OPPOSITE_PAIRS: Set[Tuple[str, str]] = {
    ("R", "S"), ("S", "R"),
    ("I", "E"), ("E", "I"),
    ("A", "C"), ("C", "A")
}

# Tipe adjacent (bersebelahan di heksagon)
ADJACENT_MAP: Dict[str, List[str]] = {
    "R": ["I", "C"],
    "I": ["R", "A"],
    "A": ["I", "S"],
    "S": ["A", "E"],
    "E": ["S", "C"],
    "C": ["E", "R"]
}

# Urutan default untuk tie-breaker
RIASEC_DEFAULT_ORDER = ["R", "I", "A", "S", "E", "C"]


# ============================================================
# FUNGSI HELPER (Bisa diuji unit secara independen)
# ============================================================

def sort_scores(scores: Dict[str, int]) -> List[Tuple[str, int]]:
    """
    Urutkan skor descending.
    
    Tie-breaker hierarki (sesuai PDF):
    1. Skor kompetensi user (jika tersedia dari data tambahan)
    2. Urutan default R-I-A-S-E-C sebagai fallback final
    
    CATATAN IMPLEMENTASI:
    Saat ini hanya menggunakan tie-breaker urutan default (langkah 2).
    Jika ke depan data skor kompetensi tersedia (misal dari asesmen tambahan),
    tambahkan parameter `competency_scores: Dict[str, int] = None` dan
    gunakan sebagai primary tie-breaker sebelum urutan default.
    
    Untuk mayoritas kasus praktis, tie-breaker urutan default sudah cukup
    karena tie exact antar tipe sangat jarang terjadi.
    
    Returns: [(type, score), ...] dari tertinggi ke terendah
    """
    return sorted(
        scores.items(),
        key=lambda x: (-x[1], RIASEC_DEFAULT_ORDER.index(x[0]))
    )


def validate_scores(scores: Dict[str, int]) -> Optional[str]:
    """
    Validasi skor untuk mendeteksi profil tidak valid / skor rendah.
    
    Range skor: per tipe 12-60 (12 soal × nilai 1-5), total 72-360.
    
    Kategori dan tindakan:
    - Semua 6 tipe identik ekstrem → HTTP 422, wajib ulang (bukan sekadar tie)
    - Severe Low (total < 120)     → HTTP 422, tidak disimpan sebagai profil final
    - Low Overall Interest (< 150) → return warning string, tetap diproses
    - Normal                        → return None
    
    CATATAN: Tie Rank1-2, Rank1-2-3, atau Rank2-3 BUKAN invalid —
    itu ditangani oleh tie-breaker di sort_scores() dan classify_riasec_code().
    Hanya "semua 6 tipe identik" yang benar-benar tidak valid dan harus ditolak.
    """
    total = sum(scores.values())
    values = list(scores.values())

    # Invalid: semua 6 tipe identik (pola ekstrem — user asal pilih semua sama)
    # Berbeda dari tie rank 1-2 atau 1-2-3 yang masih bisa diproses
    if len(set(values)) == 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Profil tidak valid: semua skor RIASEC identik. "
                "Hasil tidak dapat diproses. Silakan ulangi asesmen dengan lebih cermat."
            )
        )

    # Severe Low: total < 120 dari maksimum 360 (72 soal × nilai 5)
    if total < 120:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Skor keseluruhan terlalu rendah (total: {total} dari maksimum 360). "
                "Hasil tidak dapat disimpan sebagai profil final. "
                "Silakan ulangi asesmen."
            )
        )

    # Low Overall Interest: total < 150 — tetap diproses tapi beri peringatan
    if total < 150:
        return (
            f"Skor keseluruhan rendah (total: {total}). "
            "Hasil profil mungkin belum optimal. Disarankan untuk eksplorasi minat lebih lanjut."
        )

    return None  # Skor normal, tidak ada peringatan


def classify_riasec_code(scores: Dict[str, int]) -> Tuple[str, str, bool]:
    """
    Klasifikasi kode RIASEC: 1 huruf, 2 huruf, atau 3 huruf.
    
    Alur: cek 1 huruf → jika gagal cek 2 huruf → jika gagal fallback 3 huruf.
    
    Returns:
        Tuple[riasec_code, classification_type, is_inconsistent_profile]
        Contoh: ("RIA", "triple", False) atau ("RS", "dual", True)
    
    Aturan lengkap:
    
    KODE 1 HURUF — semua syarat harus terpenuhi:
        - Syarat 1 (Gap Absolut): rank1 - rank2 >= 9
        - Syarat 2 (Gap Relatif): (rank1 - rank2) / rank1 >= 0.15
        - Syarat 3 (Skor Minimum): rank1 >= 40
    
    KODE 2 HURUF — semua syarat harus terpenuhi:
        - Syarat 1: rank1 - rank2 < 9  (dua tipe teratas berdekatan)
        - Syarat 2: rank2 - rank3 >= 9 (ada jarak jelas antara tipe ke-2 dan ke-3)
        - Syarat 3: rank2 >= 30        (tipe kedua tidak boleh lemah)
        - Syarat 4: rank1 >= 40        (tipe pertama harus cukup kuat)
        Note: Jika rank1 dan rank2 adalah opposite → is_inconsistent = True
        
    KODE 3 HURUF (Fallback):
        - Low Differentiation: gap 1-2 < 9 DAN gap 2-3 < 9
        - Low Overall Interest: rank1 < 40
        - Forced Fallback: gagal syarat 2 huruf
    
    Bridge Table (2 huruf → 3 huruf):
        rank1 >= 40, gap 1-2 < 9, gap 2-3 >= 9, rank2 >= 30 → 2 HURUF
        rank1 >= 40, gap 1-2 < 9, gap 2-3 < 9,  rank2 >= 30 → 3 HURUF
        rank1 >= 40, gap 1-2 < 9, gap 2-3 >= 9, rank2 < 30  → 3 HURUF
        rank1 < 40,  apapun                                   → 3 HURUF

    KASUS TIE:
        - Tie Rank1-2      → bisa tetap jadi 2 huruf jika syarat terpenuhi.
                             PDF: cek skor kompetensi dulu, fallback ke R-I-A-S-E-C.
                             Brief saat ini: pakai urutan default R-I-A-S-E-C langsung
                             (lihat catatan di sort_scores tentang skor kompetensi).
        - Tie Rank1-2-3    → fallback 3 huruf otomatis (gap 1-2=0 < 9 DAN gap 2-3=0 < 9)
        - Tie Rank1-2-3-4  → low differentiation → 3 huruf. PDF: pilih 3 huruf berdasarkan
                             skor kompetensi; jika masih tied → Unranked Set.
                             Brief saat ini: tie-breaker urutan default R-I-A-S-E-C (edge case).
        - Tie Rank2-3      → rank1 tetap dominan, bisa jadi 1 huruf. Keduanya diperlakukan
                             setara di ekspansi kandidat Tier 2 dan Tier 3.
        - Tie semua 6      → sudah ditolak di validate_scores() sebelum sampai ke sini
    """
    sorted_scores = sort_scores(scores)

    rank1_type, rank1_score = sorted_scores[0]
    rank2_type, rank2_score = sorted_scores[1]
    rank3_type, rank3_score = sorted_scores[2]

    gap_1_2 = rank1_score - rank2_score
    gap_2_3 = rank2_score - rank3_score

    # ===== CEK KODE 1 HURUF =====
    if (
        rank1_score >= 40
        and gap_1_2 >= 9
        and (gap_1_2 / rank1_score) >= 0.15
    ):
        return (rank1_type, "single", False)

    # ===== CEK KODE 2 HURUF =====
    if (
        rank1_score >= 40
        and gap_1_2 < 9
        and gap_2_3 >= 9
        and rank2_score >= 30
    ):
        code = rank1_type + rank2_type
        is_inconsistent = (rank1_type, rank2_type) in OPPOSITE_PAIRS
        return (code, "dual", is_inconsistent)

    # ===== FALLBACK: KODE 3 HURUF =====
    # Termasuk kondisi: Tie Rank1-2-3 (gap keduanya = 0), Low Differentiation, Low Overall.
    # Profil 3 huruf juga bisa inkonsisten jika rank1-rank2 adalah opposite pair.
    # Dalam kasus ini split-path tetap diterapkan di ekspansi kandidat agar tidak ada
    # profesi "gabungan" yang dipaksakan dari dua kutub kepribadian yang berlawanan.
    code = rank1_type + rank2_type + rank3_type
    is_inconsistent = (rank1_type, rank2_type) in OPPOSITE_PAIRS
    return (code, "triple", is_inconsistent)


# ============================================================
# FUNGSI EKSPANSI KANDIDAT PROFESI
# ============================================================

def expand_profession_candidates(
    riasec_code: str,
    classification_type: str,
    is_inconsistent_profile: bool,
    sorted_scores: List[Tuple[str, int]],
    profession_repo: "ProfessionRepository"
) -> List[Dict[str, Any]]:
    """
    Ekspansi kandidat profesi menggunakan 4-tier algorithm.
    
    Target: 5-30 profesi disimpan (semua tier dikumpulkan).
    Dari total ini, top 3-5 (display_order 1-5) ditampilkan sebagai opsi UI Ikigai.
    Semua profesi tetap dinilai AI — termasuk yang tidak ditampilkan sebagai opsi,
    dipakai sebagai backup scoring saat user tidak memilih opsi apapun.

    CATATAN — 30 kandidat vs PDF maks 5:
    PDF menyebut "minimal 3, maksimal 5 profesi" untuk opsi UI.
    Brief ini menyimpan hingga 30 profesi karena Ikigai butuh pool kandidat lebih besar
    untuk scoring AI — termasuk profesi yang tidak ditampilkan sebagai opsi (backup scoring).
    Ini konsisten dengan prinsip "compute all, display top-N" di bagian Ikigai PDF.
    Yang ditampilkan ke user sebagai opsi pilihan tetap hanya top 3-5 (display_order <= 5).
    
    PENTING — Perbedaan Tier 2 untuk profil dual vs triple:

    Profil DUAL (2 huruf, misal RI):
      - Lapisan Primer: RI dan IR diperlakukan setara (gap kecil, urutan tidak signifikan)
      - Lapisan Sekunder: tambah huruf ketiga (Rank3) yang bukan opposite → RIA, IRA, dst
        Huruf ketiga masuk SETELAH lapisan primer, tidak dicampur dari awal.

    Profil TRIPLE (3 huruf, misal RIA):
      - Semua 6 permutasi (3! = 6) langsung dianggap setara — Unranked Set.
      - Tidak ada prioritas urutan karena gap antar ketiganya kecil.

    Tie Rank2-Rank3: kedua huruf diperlakukan setara di Tier 2 dan Tier 3.
    """
    if is_inconsistent_profile and len(riasec_code) >= 2:
        return _expand_split_path(riasec_code, sorted_scores, profession_repo)

    top_3_types = [t for t, _ in sorted_scores[:3]]
    rank2_score = sorted_scores[1][1]
    rank3_score = sorted_scores[2][1]

    candidates = []
    seen_ids: Set[int] = set()
    display_order = 1

    # === TIER 1: Exact Match ===
    for p in profession_repo.find_by_riasec_code(riasec_code):
        if p.id not in seen_ids:
            candidates.append(_build_candidate(p, 1, "exact_match", 1.0, display_order))
            seen_ids.add(p.id)
            display_order += 1

    # === TIER 2: Kode Kongruen ===
    if len(candidates) < 30:
        if classification_type == "dual":
            # Profil 2 huruf: Lapisan Primer (permutasi 2 huruf saja: RI dan IR)
            letter_a, letter_b = riasec_code[0], riasec_code[1]
            for pcode in [letter_a + letter_b, letter_b + letter_a]:
                if pcode != riasec_code:
                    for p in profession_repo.find_by_riasec_code(pcode):
                        if p.id not in seen_ids:
                            candidates.append(_build_candidate(p, 2, "congruent_primer", 0.95, display_order))
                            seen_ids.add(p.id)
                            display_order += 1

            # Lapisan Sekunder: tambah huruf ketiga yang bukan opposite
            rank3_type = top_3_types[2]
            opposite_of_a = next((b for a, b in OPPOSITE_PAIRS if a == letter_a), None)
            opposite_of_b = next((b for a, b in OPPOSITE_PAIRS if a == letter_b), None)
            if rank3_type not in {opposite_of_a, opposite_of_b}:
                for scode in [letter_a + letter_b + rank3_type, letter_b + letter_a + rank3_type]:
                    for p in profession_repo.find_by_riasec_code(scode):
                        if p.id not in seen_ids:
                            candidates.append(_build_candidate(p, 2, "congruent_secondary", 0.88, display_order))
                            seen_ids.add(p.id)
                            display_order += 1
        else:
            # Profil 3 huruf: Unranked Set — semua 6 permutasi setara
            for perm_code in ["".join(p) for p in permutations(top_3_types) if "".join(p) != riasec_code]:
                for p in profession_repo.find_by_riasec_code(perm_code):
                    if p.id not in seen_ids:
                        is_adj = _first_two_adjacent(perm_code)
                        ctype = "congruent_adjacent" if is_adj else "congruent_permutation"
                        candidates.append(_build_candidate(p, 2, ctype, 0.95 if is_adj else 0.85, display_order))
                        seen_ids.add(p.id)
                        display_order += 1

    # === TIER 3: Subset 2 Huruf dari Top 3 ===
    # Jika Rank2-Rank3 tied, semua subset diperlakukan setara
    if len(candidates) < 30:
        for subset_code in ["".join(pair) for pair in combinations(top_3_types, 2)]:
            for p in profession_repo.find_by_riasec_code(subset_code):
                if p.id not in seen_ids:
                    is_adj = _letters_adjacent(subset_code[0], subset_code[1])
                    ctype = "subset_adjacent" if is_adj else "subset_alternate"
                    candidates.append(_build_candidate(p, 3, ctype, 0.75 if is_adj else 0.65, display_order))
                    seen_ids.add(p.id)
                    display_order += 1

    # === TIER 4: Huruf Dominan Tunggal ===
    if len(candidates) < 30:
        for p in profession_repo.find_by_riasec_code(top_3_types[0]):
            if p.id not in seen_ids:
                candidates.append(_build_candidate(p, 4, "dominant_single", 0.55, display_order))
                seen_ids.add(p.id)
                display_order += 1

    return candidates[:20]


def _expand_split_path(
    riasec_code: str,
    sorted_scores: List[Tuple[str, int]],
    profession_repo: "ProfessionRepository"
) -> List[Dict[str, Any]]:
    """
    Split-Path Strategy untuk profil inkonsisten (opposite pair: RS, IE, atau AC).
    
    Dua huruf opposite diperlakukan sebagai dua jalur terpisah.
    Tidak dipaksakan jadi satu profesi gabungan karena tidak ada profesi
    yang benar-benar cocok untuk kepribadian yang saling berlawanan.
    
    Path A: huruf pertama + adjacent-nya
    Path B: huruf kedua + adjacent-nya
    
    Contoh profil RS (R opposite S):
    - Path A: cari profesi R, RI, RC
    - Path B: cari profesi S, SA, SE
    
    Tag path="A" atau path="B" dikirim ke Flutter agar bisa tampilkan
    narasi "Profilmu mencakup dua kutub yang berbeda..."
    """
    letter_a = riasec_code[0]
    letter_b = riasec_code[1]
    candidates = []
    seen_ids: Set[int] = set()
    display_order = 1

    def expand_one_path(letter: str, path_label: str):
        nonlocal display_order

        # Exact match huruf tunggal
        for p in profession_repo.find_by_riasec_code(letter):
            if p.id not in seen_ids:
                c = _build_candidate(p, 1, "exact_match", 1.0, display_order)
                c["path"] = path_label
                candidates.append(c)
                seen_ids.add(p.id)
                display_order += 1

        # Adjacent 2-huruf: cari KEDUA urutan (letter+adj dan adj+letter)
        # karena profil non-split memperlakukan RI dan IR setara,
        # split-path juga perlu konsisten mencari kedua arah.
        for adj in ADJACENT_MAP.get(letter, []):
            for code2 in [letter + adj, adj + letter]:
                for p in profession_repo.find_by_riasec_code(code2):
                    if p.id not in seen_ids:
                        c = _build_candidate(p, 2, "congruent_adjacent", 0.85, display_order)
                        c["path"] = path_label
                        candidates.append(c)
                        seen_ids.add(p.id)
                        display_order += 1

    expand_one_path(letter_a, "A")
    expand_one_path(letter_b, "B")
    return candidates[:20]


def _build_candidate(profession, tier: int, ctype: str, score: float, order: int) -> Dict:
    """
    Buat dict kandidat profesi untuk disimpan di JSONB candidates_data.

    CATATAN — Model Profession & ProfessionRepository:
    Fungsi ini mengasumsikan objek `profession` punya field .id dan .riasec_code_id.
    Model Profession dan ProfessionRepository tidak didefinisikan di brief ini
    karena scope-nya adalah RIASEC saja — profesi belum relevan di tahap ini.
    Penjelasan lengkap model Profession, FK ke riasec_codes, dan implementasi
    ProfessionRepository akan dibahas di Brief Part 2 (Ikigai).
    """
    return {
        "profession_id": profession.id,
        "riasec_code_id": profession.riasec_code_id,
        "expansion_tier": tier,
        "congruence_type": ctype,
        "congruence_score": score,
        "display_order": order,
        # Opsi soal = display_order 1-5 (Tier 1 diprioritaskan, min 3 maks 5)
        # Backup scoring = display_order 6-20 (dinilai AI hanya jika user tidak memilih)
        "is_display_candidate": order <= 5,
        # "path" hanya ditambahkan jika is_inconsistent_profile=True (oleh pemanggil)
    }


def _first_two_adjacent(code: str) -> bool:
    """Cek apakah 2 huruf pertama kode bersifat adjacent di heksagon."""
    if len(code) < 2:
        return False
    return code[1] in ADJACENT_MAP.get(code[0], [])


def _letters_adjacent(a: str, b: str) -> bool:
    """Cek apakah dua huruf RIASEC bersifat adjacent."""
    return b in ADJACENT_MAP.get(a, [])


# ============================================================
# RIASEC SERVICE CLASS
# ============================================================

class RIASECService:
    """
    Orchestrator untuk seluruh alur submit RIASEC:
    validasi → kalkulasi → klasifikasi → simpan → ekspansi kandidat
    """

    def __init__(self, db: Session):
        self.db = db
        self.profession_repo = ProfessionRepository(db)

    def submit_riasec_test(
        self,
        user: User,
        session_token: str,
        responses: List[RIASECAnswerItem]
    ) -> dict:
        """
        Main method: terima 72 jawaban (12 per tipe), proses semua, return hasil lengkap.
        
        Alur di dalamnya:
        1. Validasi sesi (token valid, status benar, milik user ini)
        2. Validasi question_ids sesuai yang di-generate
        3. Hitung skor mentah (raw sum per tipe)
        4. Validasi skor (red flag check)
        5. Klasifikasi kode RIASEC
        6. Lookup detail kode dari tabel riasec_codes
        7. INSERT riasec_responses
        8. INSERT riasec_results
        9. Ekspansi kandidat profesi (4-tier / split-path)
        10. INSERT ikigai_candidate_professions
        11. UPDATE status sesi → riasec_completed
        12. Jika FIT_CHECK: UPDATE kenalidiri_history → completed, sesi → completed
        13. Return hasil lengkap
        """
        # 1. Validasi sesi
        session = self._validate_session(session_token, user)

        # 2. Validasi question_ids
        self._validate_question_ids(session.id, responses)

        # 3. Hitung skor
        scores = self._calculate_scores(responses)

        # 4. Validasi skor (raise jika invalid/severe, return warning jika low)
        validity_warning = validate_scores(scores)

        # 5. Klasifikasi kode RIASEC
        riasec_code, classification_type, is_inconsistent = classify_riasec_code(scores)

        # 6. Lookup detail kode dari database
        code_obj = self._get_riasec_code(riasec_code)

        # 7. Simpan jawaban
        self._save_responses(session.id, responses)

        # 8. Simpan hasil klasifikasi
        riasec_result = self._save_result(session.id, scores, code_obj.id, classification_type, is_inconsistent)

        # 9. Ekspansi kandidat profesi
        sorted_sc = sort_scores(scores)
        candidates = expand_profession_candidates(
            riasec_code=riasec_code,
            classification_type=classification_type,
            is_inconsistent_profile=is_inconsistent,
            sorted_scores=sorted_sc,
            profession_repo=self.profession_repo
        )

        # Peringatan jika kandidat kurang dari 3 (setelah semua tier)
        if len(candidates) < 3 and not validity_warning:
            validity_warning = (
                f"Hanya ditemukan {len(candidates)} profesi kandidat. "
                "Disarankan untuk eksplorasi minat lebih lanjut."
            )

        # 10. Simpan kandidat
        self._save_candidates(session.id, riasec_code, code_obj.id, scores, candidates, is_inconsistent)

        # 11. Update status sesi → riasec_completed
        self._mark_riasec_completed(session)

        # 12. Tentukan next step dan update history jika FIT_CHECK
        if session.test_goal == "FIT_CHECK":
            self._mark_fit_check_completed(session, riasec_result)
            next_step = "fit_check_result"
        else:
            next_step = "ikigai"

        # Hitung berapa yang ditampilkan sebagai opsi UI (display_order 1-5)
        display_count = len([c for c in candidates if c["display_order"] <= 5])

        self.db.commit()

        return {
            "session_token": session_token,
            "test_goal": session.test_goal,
            "status": session.status,
            "scores": {
                "R": scores["R"], "I": scores["I"], "A": scores["A"],
                "S": scores["S"], "E": scores["E"], "C": scores["C"]
            },
            "classification_type": classification_type,
            "is_inconsistent_profile": is_inconsistent,
            "riasec_code_info": {
                "riasec_code": code_obj.riasec_code,
                "riasec_title": code_obj.riasec_title,
                "riasec_description": code_obj.riasec_description,
                "strengths": code_obj.strengths or [],
                "challenges": code_obj.challenges or [],
                "strategies": code_obj.strategies or [],
                "work_environments": code_obj.work_environments or [],
                "interaction_styles": code_obj.interaction_styles or [],
            },
            "candidates": candidates,
            "total_candidates": len(candidates),
            "display_candidates_count": display_count,
            "validity_warning": validity_warning,
            "next_step": next_step
        }

    # ============================================================
    # PRIVATE HELPERS
    # ============================================================

    def _validate_session(self, session_token: str, user: User) -> CareerProfileTestSession:
        """Validasi sesi: ada, milik user ini, dan statusnya riasec_ongoing."""
        session = self.db.query(CareerProfileTestSession).filter(
            CareerProfileTestSession.session_token == session_token
        ).first()

        if not session:
            raise HTTPException(status_code=404, detail="Session token tidak ditemukan")

        if str(session.user_id) != str(user.id):
            raise HTTPException(
                status_code=403,
                detail="Session ini bukan milik user yang sedang login"
            )

        if session.status != "riasec_ongoing":
            if session.status == "riasec_completed":
                detail_msg = "RIASEC sudah pernah disubmit untuk sesi ini. Gunakan GET /riasec/result/{token} untuk melihat hasilnya."
            elif session.status == "completed":
                detail_msg = "Sesi ini sudah selesai sepenuhnya."
            else:
                detail_msg = f"Status sesi tidak valid untuk submit RIASEC: '{session.status}'."
            raise HTTPException(status_code=400, detail=detail_msg)

        return session

    def _validate_question_ids(self, session_id: int, responses: List[RIASECAnswerItem]):
        """
        Pastikan question_id yang dikirim user persis sama dengan
        yang di-generate di awal sesi (tersimpan di riasec_question_sets).
        Total harus tepat 72 ID, tidak boleh ada duplikat.
        """
        question_set = self.db.query(RIASECQuestionSet).filter(
            RIASECQuestionSet.test_session_id == session_id
        ).first()

        if not question_set:
            raise HTTPException(
                status_code=404,
                detail="Question set tidak ditemukan untuk sesi ini. Mulai ulang sesi."
            )

        provided_ids = [r.question_id for r in responses]
        provided_ids_set = set(provided_ids)

        # Cek duplikat question_id — set() menghilangkan duplikat,
        # jadi 73 jawaban dengan satu ID double akan kelihatan seperti 72 unik
        # tanpa pengecekan ini. Flutter harusnya tidak kirim duplikat tapi tetap harus dicegah.
        if len(provided_ids) != len(provided_ids_set):
            dupes = [qid for qid in provided_ids_set if provided_ids.count(qid) > 1]
            raise HTTPException(
                status_code=400,
                detail=f"Terdapat question_id yang dikirim lebih dari satu kali: {dupes}"
            )

        expected_ids = set(question_set.question_ids)

        if expected_ids != provided_ids_set:
            missing = expected_ids - provided_ids_set
            extra = provided_ids_set - expected_ids
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Question ID tidak sesuai dengan soal yang diberikan. "
                    f"Kurang: {missing}, Berlebih: {extra}"
                )
            )

    def _calculate_scores(self, responses: List[RIASECAnswerItem]) -> Dict[str, int]:
        """
        Hitung skor mentah (RAW SUM) per tipe RIASEC.
        
        PENTING — Gunakan RAW SUM, BUKAN rata-rata:
        - 12 soal per tipe, nilai 1-5 per soal
        - Range skor per tipe: 12-60
        - Skor total range: 72-360
        
        Threshold klasifikasi (sesuai PDF):
        - Rank1 >= 40  → valid untuk kode 1 atau 2 huruf
        - Total < 120  → Severe Low (HTTP 422)
        - Total < 150  → Low Overall Interest (warning)
        
        question_type di setiap response dikirim langsung oleh Flutter
        berdasarkan data riasec_questions.json (tipe soal sudah diketahui Flutter).
        """
        scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
        for r in responses:
            scores[r.question_type] += r.answer_value
        return scores

    def _get_riasec_code(self, riasec_code: str) -> RIASECCode:
        """Ambil detail kode RIASEC dari tabel riasec_codes."""
        code_obj = self.db.query(RIASECCode).filter(
            RIASECCode.riasec_code == riasec_code
        ).first()

        if not code_obj:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Kode RIASEC '{riasec_code}' tidak ditemukan di database. "
                    "Pastikan seed data riasec_codes sudah dijalankan (scripts/seed_riasec_codes.py)."
                )
            )
        return code_obj

    def _save_responses(self, session_id: int, responses: List[RIASECAnswerItem]):
        """INSERT ke riasec_responses — satu baris per sesi, tidak pernah di-update."""
        responses_data = {
            "responses": [
                {
                    "question_id": r.question_id,
                    "question_type": r.question_type,
                    "answer_value": r.answer_value,
                    "answered_at": r.answered_at.isoformat()
                }
                for r in responses
            ],
            "total_questions": 72,
            "completed": True,
            "submitted_at": datetime.utcnow().isoformat()
        }

        response_record = RIASECResponse(
            test_session_id=session_id,
            responses_data=responses_data
        )
        self.db.add(response_record)

    def _save_result(
        self,
        session_id: int,
        scores: Dict[str, int],
        riasec_code_id: int,
        classification_type: str,
        is_inconsistent: bool
    ):
        """INSERT ke riasec_results."""
        result = RIASECResult(
            test_session_id=session_id,
            score_r=scores["R"],
            score_i=scores["I"],
            score_a=scores["A"],
            score_s=scores["S"],
            score_e=scores["E"],
            score_c=scores["C"],
            riasec_code_id=riasec_code_id,
            riasec_code_type=classification_type,
            is_inconsistent_profile=is_inconsistent
        )
        self.db.add(result)
        self.db.flush()
        return result

    def _save_candidates(
        self,
        session_id: int,
        riasec_code: str,
        riasec_code_id: int,
        scores: Dict[str, int],
        candidates: List[Dict],
        is_inconsistent: bool
    ):
        """
        INSERT ke ikigai_candidate_professions.
        
        Satu baris JSONB per sesi. IMMUTABLE — tidak pernah di-UPDATE setelah ini.
        
        Kolom candidates_data berisi metadata lengkap untuk keperluan Ikigai service:
        - Semua kandidat (5-30 profesi)
        - Metadata ekspansi
        - Strategi yang digunakan (4_tier_expansion atau split_path)
        """
        expansion_strategy = "split_path" if is_inconsistent else "4_tier_expansion"

        candidates_data = {
            "candidates": candidates,
            "metadata": {
                "total_candidates": len(candidates),
                "user_riasec_code_id": riasec_code_id,
                "user_riasec_code": riasec_code,
                "user_riasec_scores": scores,
                "is_inconsistent_profile": is_inconsistent,
                "expansion_strategy": expansion_strategy,
                "expansion_summary": {
                    "tier_1_exact": sum(1 for c in candidates if c["expansion_tier"] == 1),
                    "tier_2_congruent": sum(1 for c in candidates if c["expansion_tier"] == 2),
                    "tier_3_subset": sum(1 for c in candidates if c["expansion_tier"] == 3),
                    "tier_4_dominant": sum(1 for c in candidates if c["expansion_tier"] == 4),
                },
                "display_count": len([c for c in candidates if c["display_order"] <= 5]),
                "generated_at": datetime.utcnow().isoformat()
            }
        }

        candidate_record = IkigaiCandidateProfession(
            test_session_id=session_id,
            candidates_data=candidates_data,
            total_candidates=len(candidates),
            generation_strategy=expansion_strategy,
        )
        self.db.add(candidate_record)


    def _mark_riasec_completed(self, session: CareerProfileTestSession):
        """Update status sesi ke riasec_completed dan isi timestamp."""
        session.status = "riasec_completed"
        session.riasec_completed_at = datetime.utcnow()

    def _mark_fit_check_completed(self, session: CareerProfileTestSession, riasec_result: RIASECResult):
        """
        Untuk FIT_CHECK: override status riasec_completed → completed sekaligus.

        CATATAN ALUR STATUS:
        _mark_riasec_completed() dipanggil duluan → status = "riasec_completed" (in-memory).
        Method ini lalu override ke "completed" sebelum commit terjadi.
        Jadi di database, status langsung masuk sebagai "completed" — tidak pernah
        tersimpan sebagai "riasec_completed" untuk sesi FIT_CHECK.

        Alur status FIT_CHECK (in-memory sebelum commit):
          riasec_ongoing → riasec_completed → completed  (hanya completed yang ter-commit)

        Alur status RECOMMENDATION:
          riasec_ongoing → riasec_completed  (ter-commit di sini)
          → ikigai_ongoing → ikigai_completed → completed  (di-commit di Ikigai service)
        """
        session.status = "completed"
        session.completed_at = datetime.utcnow()

        # Update kenalidiri_history
        from app.db.models.kenalidiri_history import KenaliDiriHistory
        history = self.db.query(KenaliDiriHistory).filter(
            KenaliDiriHistory.detail_session_id == session.id
        ).first()
        if history:
            history.status = "completed"
            history.completed_at = datetime.utcnow()
            
        # === TAMBAHAN BARU: INSERT fit_check_results ===
        self._insert_fit_check_result(session, riasec_result)

    def _insert_fit_check_result(self, session: CareerProfileTestSession, riasec_result: RIASECResult):
        """
        Hitung rule-based classification dan INSERT ke fit_check_results.
        Dipanggil hanya untuk sesi FIT_CHECK setelah RIASEC selesai.
        """
        from app.api.v1.features.career_profile.models.result import FitCheckResult
        from app.api.v1.features.career_profile.services.fit_check_classifier import classify_fit_check
        from app.api.v1.features.career_profile.models.riasec import RIASECCode
        from app.models.profession import Profession as TargetProfession

        user_code_obj = self.db.query(RIASECCode).filter(
            RIASECCode.id == riasec_result.riasec_code_id
        ).first()
        if not user_code_obj:
            raise HTTPException(
                status_code=500,
                detail=f"riasec_codes tidak ditemukan untuk riasec_code_id={riasec_result.riasec_code_id}. Pastikan seed data riasec_codes sudah dijalankan."
            )

        # Ambil kode RIASEC profesi target
        profession = self.db.query(TargetProfession).filter(
            TargetProfession.id == session.target_profession_id
        ).first()
        if not profession:
            raise HTTPException(status_code=404, detail=f"Profesi target ID {session.target_profession_id} tidak ditemukan")

        prof_code_obj = self.db.query(RIASECCode).filter(
            RIASECCode.id == profession.riasec_code_id
        ).first()
        if not prof_code_obj:
            raise HTTPException(
                status_code=500,
                detail=f"riasec_codes tidak ditemukan untuk profesi ID={session.target_profession_id} (riasec_code_id={profession.riasec_code_id}). Pastikan data profesi sudah memiliki riasec_code yang valid."
            )

        # Klasifikasi
        classification = classify_fit_check(
            user_riasec_code=user_code_obj.riasec_code,
            profession_riasec_code=prof_code_obj.riasec_code
        )

        fit_check_record = FitCheckResult(
            test_session_id=session.id,
            profession_id=session.target_profession_id,
            user_riasec_code_id=riasec_result.riasec_code_id,
            profession_riasec_code_id=prof_code_obj.id,
            match_category=classification["match_category"],
            rule_type=classification["rule_type"],
            dominant_letter_same=classification.get("dominant_letter_same", False),
            is_adjacent_hexagon=classification.get("is_adjacent_hexagon", False),
            match_score=classification.get("match_score")
        )
        self.db.add(fit_check_record)

    def get_result(self, session_token: str, user: User) -> dict:
        """Ambil hasil RIASEC yang sudah tersimpan untuk reload halaman."""
        session = self.db.query(CareerProfileTestSession).filter(
            CareerProfileTestSession.session_token == session_token
        ).first()

        if not session or str(session.user_id) != str(user.id):
            raise HTTPException(
                status_code=404,
                detail="Sesi tidak ditemukan atau bukan milik user ini"
            )

        result = self.db.query(RIASECResult).filter(
            RIASECResult.test_session_id == session.id
        ).first()

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Hasil RIASEC belum tersedia untuk sesi ini"
            )

        code_obj = self.db.query(RIASECCode).filter(
            RIASECCode.id == result.riasec_code_id
        ).first()

        candidates_record = self.db.query(IkigaiCandidateProfession).filter(
            IkigaiCandidateProfession.test_session_id == session.id
        ).first()

        candidates = []
        if candidates_record:
            candidates = candidates_record.candidates_data.get("candidates", [])

        display_count = len([c for c in candidates if c.get("display_order", 99) <= 5])
        next_step = "ikigai" if session.test_goal == "RECOMMENDATION" else "fit_check_result"

        self.db.commit()

        # ── AUTO-SAVE user_career_profiles (AKHIR RIASEC / FIT-CHECK) ──────
        try:
            # Hanya auto-save jika FIT_CHECK (karena RECOMMENDATION nunggu Ikigai)
            if session.test_goal == "FIT_CHECK":
                from app.api.v1.features.career_profile.services.user_career_profile_service import UserCareerProfileService
                _ucp_svc = UserCareerProfileService(self.db)
                
                from app.api.v1.features.career_profile.models.result import FitCheckResult
                fit_res = self.db.query(FitCheckResult).filter(FitCheckResult.test_session_id == session.id).first()
                t_prof_id = fit_res.profession_id if fit_res else None

                _ucp_svc.auto_save_if_first(
                    user_id=session.user_id,
                    session=session,
                    top_profession1_id=t_prof_id,
                    top_profession2_id=None,
                    riasec_code=code_obj.riasec_code,
                )
                # Commit profil aktif secara terpisah
                self.db.commit()
        except Exception:
            self.db.rollback()

        return {
            "session_token": session_token,
            "test_goal": session.test_goal,
            "status": session.status,
            "scores": {
                "R": result.score_r, "I": result.score_i, "A": result.score_a,
                "S": result.score_s, "E": result.score_e, "C": result.score_c
            },
            "classification_type": result.riasec_code_type,
            "is_inconsistent_profile": result.is_inconsistent_profile,
            "riasec_code_info": {
                "riasec_code": code_obj.riasec_code,
                "riasec_title": code_obj.riasec_title,
                "riasec_description": code_obj.riasec_description,
                "strengths": code_obj.strengths or [],
                "challenges": code_obj.challenges or [],
                "strategies": code_obj.strategies or [],
                "work_environments": code_obj.work_environments or [],
                "interaction_styles": code_obj.interaction_styles or [],
            },
            "candidates": candidates,
            "total_candidates": len(candidates),
            "display_candidates_count": display_count,
            "validity_warning": None,
            "next_step": next_step
        }
