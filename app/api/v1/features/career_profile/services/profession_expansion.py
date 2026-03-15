# app/api/v1/categories/career_profile/services/profession_expansion.py
"""
Profession Expansion Service — Logika Kandidat Ikigai

ATURAN KANDIDAT (diperbarui):
─────────────────────────────
KANDIDAT OPSI (display_order 1–5):
  - Profesi yang MUNCUL sebagai pilihan soal di Flutter
  - Prioritas: kode PERSIS SAMA dengan kode RIASEC user (Tier 1)
  - Jumlah: min 3, maks 5
  - Jika Tier 1 < 3 profesi, isi sisa slot dari Tier 2 (kode kongruen)

KANDIDAT BACKUP (display_order 6–20):
  - Profesi yang TIDAK tampil sebagai opsi soal
  - Hanya dinilai oleh scoring AI jika user TIDAK memilih opsi apapun
    pada satu atau beberapa dimensi (sebagai safeguard)
  - Sumber: kode kongruen (permutasi + subset + dominan)
  - Total kandidat (opsi + backup): MAKS 20

SUMBER KODE KONGRUEN:
  Tier 2 — semua permutasi dari 3 huruf top user (misal IRA → RAI, AIR, dst.)
  Tier 3 — subset 2-huruf dari top 3 (RI, RA, IA, IR, AI, AR)
  Tier 4 — huruf dominan tunggal (R)
"""

from itertools import permutations
from typing import Dict, List, Any, Set
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.api.v1.features.career_profile.repositories.profession_repo import (
    ProfessionRepository,
    Profession,
)
from app.api.v1.features.career_profile.repositories.riasec_repo import RIASECRepository
from app.api.v1.features.career_profile.models.profession import IkigaiCandidateProfession

# ──────────────────────────────────────────────────────────────────────
# Konstanta
# ──────────────────────────────────────────────────────────────────────
MAX_DISPLAY_CANDIDATES = 5   # Maks yang muncul sebagai opsi soal
MIN_DISPLAY_CANDIDATES = 3   # Min yang muncul sebagai opsi soal
MAX_TOTAL_CANDIDATES   = 20  # Maks total (opsi + backup)

HEXAGON_ADJACENT = {
    'R': ['I', 'C'],
    'I': ['R', 'A'],
    'A': ['I', 'S'],
    'S': ['A', 'E'],
    'E': ['S', 'C'],
    'C': ['E', 'R'],
}


class ProfessionExpansionService:
    """
    Service untuk menghasilkan daftar kandidat profesi Ikigai.

    Output berisi 2 kelompok:
      1. Kandidat OPSI   (display_order 1–5, is_display_candidate=True)
         → ditampilkan sebagai pilihan soal di Flutter
      2. Kandidat BACKUP (display_order 6–20, is_display_candidate=False)
         → dinilai AI hanya jika user tidak memilih opsi apapun di suatu dimensi
    """

    def __init__(self, db: Session):
        self.db = db
        self.profession_repo = ProfessionRepository(db)
        self.riasec_repo = RIASECRepository(db)

    # ─────────────────────────────────────────────────────────────────
    # PUBLIC: expand_candidates
    # ─────────────────────────────────────────────────────────────────

    def expand_candidates(
        self,
        riasec_code: str,
        riasec_code_id: int,
        user_scores: Dict[str, int],
        is_inconsistent_profile: bool = False,
    ) -> Dict[str, Any]:
        """
        Hasilkan daftar kandidat profesi untuk sesi Ikigai.

        Args:
            riasec_code        : Kode RIASEC user (misal "RIA")
            riasec_code_id     : FK id dari tabel riasec_codes
            user_scores        : Skor mentah per tipe {"R": 54, "I": 52, ...}
            is_inconsistent_profile: True jika user punya tipe berlawanan (R-S, I-E, A-C)

        Returns:
            Dict JSONB yang akan disimpan ke ikigai_candidate_professions.candidates_data
        """
        sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
        top_3_types = [t[0] for t in sorted_scores[:3]]

        if is_inconsistent_profile and len(riasec_code) >= 2:
            return self._expand_split_path(riasec_code, user_scores, top_3_types)

        return self._expand_standard(
            riasec_code, riasec_code_id, user_scores, top_3_types
        )

    # ─────────────────────────────────────────────────────────────────
    # STANDARD EXPANSION
    # ─────────────────────────────────────────────────────────────────

    def _expand_standard(
        self,
        riasec_code: str,
        riasec_code_id: int,
        user_scores: Dict[str, int],
        top_3_types: List[str],
    ) -> Dict[str, Any]:
        seen: Set[int] = set()
        display_candidates: List[Dict] = []   # Tier 1 → opsi soal
        backup_candidates:  List[Dict] = []   # Tier 2/3/4 → backup scoring

        expansion_summary = {
            "tier_1_count": 0,
            "tier_2_count": 0,
            "tier_3_count": 0,
            "tier_4_count": 0,
            "total_unique":  0,
            "display_count": 0,
            "backup_count":  0,
        }

        # ── TIER 1: Exact Match → kandidat OPSI ──────────────────────
        tier1 = self._query_by_code_id(riasec_code_id, seen, limit=MAX_DISPLAY_CANDIDATES)
        for p in tier1:
            display_candidates.append(self._make_entry(
                p, riasec_code_id,
                tier=1, congruence_type="exact_match", congruence_score=1.0,
                display_order=len(display_candidates) + 1,
                is_display=True,
            ))
        expansion_summary["tier_1_count"] = len(tier1)

        # ── TIER 2: Kongruen → isi sisa slot OPSI, sisanya BACKUP ────
        congruent_codes = self._generate_congruent_codes(riasec_code, top_3_types)
        tier2_professions = self._query_by_code_strings(
            congruent_codes, seen,
            limit=MAX_TOTAL_CANDIDATES,  # ambil banyak dulu, nanti dibagi
        )
        for p in tier2_professions:
            if len(display_candidates) < MAX_DISPLAY_CANDIDATES:
                # Masih ada slot opsi kosong (karena Tier 1 < 3/5)
                display_candidates.append(self._make_entry(
                    p, p.riasec_code_id,
                    tier=2, congruence_type="congruent", congruence_score=0.8,
                    display_order=len(display_candidates) + 1,
                    is_display=True,
                ))
            else:
                # Slot opsi penuh → masukkan backup
                backup_order = MAX_DISPLAY_CANDIDATES + len(backup_candidates) + 1
                if backup_order <= MAX_TOTAL_CANDIDATES:
                    backup_candidates.append(self._make_entry(
                        p, p.riasec_code_id,
                        tier=2, congruence_type="congruent", congruence_score=0.8,
                        display_order=backup_order,
                        is_display=False,
                    ))
        expansion_summary["tier_2_count"] = len(tier2_professions)

        # ── TIER 3: Subset codes → BACKUP ────────────────────────────
        if len(display_candidates) + len(backup_candidates) < MAX_TOTAL_CANDIDATES:
            subset_codes = self._generate_subset_codes(top_3_types)
            tier3_professions = self._query_by_code_strings(
                subset_codes, seen,
                limit=MAX_TOTAL_CANDIDATES - len(display_candidates) - len(backup_candidates),
            )
            for p in tier3_professions:
                if len(display_candidates) < MAX_DISPLAY_CANDIDATES:
                    display_candidates.append(self._make_entry(
                        p, p.riasec_code_id,
                        tier=3, congruence_type="subset", congruence_score=0.6,
                        display_order=len(display_candidates) + 1,
                        is_display=True,
                    ))
                else:
                    backup_order = MAX_DISPLAY_CANDIDATES + len(backup_candidates) + 1
                    if backup_order <= MAX_TOTAL_CANDIDATES:
                        backup_candidates.append(self._make_entry(
                            p, p.riasec_code_id,
                            tier=3, congruence_type="subset", congruence_score=0.6,
                            display_order=backup_order,
                            is_display=False,
                        ))
            expansion_summary["tier_3_count"] = len(tier3_professions)

        # ── TIER 4: Dominant single → BACKUP ─────────────────────────
        total_so_far = len(display_candidates) + len(backup_candidates)
        if total_so_far < MAX_TOTAL_CANDIDATES and len(display_candidates) < MIN_DISPLAY_CANDIDATES:
            dominant_type = riasec_code[0]
            tier4_professions = self._query_by_code_string(
                dominant_type, seen,
                limit=MAX_TOTAL_CANDIDATES - total_so_far,
            )
            for p in tier4_professions:
                if len(display_candidates) < MAX_DISPLAY_CANDIDATES:
                    display_candidates.append(self._make_entry(
                        p, p.riasec_code_id,
                        tier=4, congruence_type="dominant_single", congruence_score=0.4,
                        display_order=len(display_candidates) + 1,
                        is_display=True,
                    ))
                else:
                    backup_order = MAX_DISPLAY_CANDIDATES + len(backup_candidates) + 1
                    if backup_order <= MAX_TOTAL_CANDIDATES:
                        backup_candidates.append(self._make_entry(
                            p, p.riasec_code_id,
                            tier=4, congruence_type="dominant_single", congruence_score=0.4,
                            display_order=backup_order,
                            is_display=False,
                        ))
            expansion_summary["tier_4_count"] = len(tier4_professions)

        all_candidates = display_candidates + backup_candidates
        expansion_summary["display_count"] = len(display_candidates)
        expansion_summary["backup_count"]  = len(backup_candidates)
        expansion_summary["total_unique"]  = len(seen)

        return {
            "user_riasec_code":        riasec_code,
            "user_top_3_types":        top_3_types,
            "user_scores":             user_scores,
            "is_inconsistent_profile": False,
            "candidates":              all_candidates,
            "expansion_summary":       expansion_summary,
        }

    # ─────────────────────────────────────────────────────────────────
    # SPLIT-PATH EXPANSION (profil inkonsisten, misal R-S atau I-E)
    # ─────────────────────────────────────────────────────────────────

    def _expand_split_path(
        self,
        riasec_code: str,
        user_scores: Dict[str, int],
        top_3_types: List[str],
    ) -> Dict[str, Any]:
        type_a = riasec_code[0]
        type_b = riasec_code[1]
        seen: Set[int] = set()
        display_candidates: List[Dict] = []
        backup_candidates:  List[Dict] = []

        expansion_summary = {
            "path_a_count": 0, "path_b_count": 0,
            "display_count": 0, "backup_count": 0, "total_unique": 0,
        }

        def _add_from_codes(codes: List[str], path: str):
            for code_str in codes:
                profs = self._query_by_code_string(code_str, seen, limit=5)
                for p in profs:
                    score = 0.9 if len(code_str) == 1 else 0.7
                    if len(display_candidates) < MAX_DISPLAY_CANDIDATES:
                        display_candidates.append(self._make_entry(
                            p, p.riasec_code_id,
                            tier=None, congruence_type="split_path", congruence_score=score,
                            display_order=len(display_candidates) + 1,
                            is_display=True, extra={"path": path, "matched_code": code_str},
                        ))
                    else:
                        bo = MAX_DISPLAY_CANDIDATES + len(backup_candidates) + 1
                        if bo <= MAX_TOTAL_CANDIDATES:
                            backup_candidates.append(self._make_entry(
                                p, p.riasec_code_id,
                                tier=None, congruence_type="split_path", congruence_score=score,
                                display_order=bo,
                                is_display=False, extra={"path": path, "matched_code": code_str},
                            ))
                total = len(display_candidates) + len(backup_candidates)
                if total >= MAX_TOTAL_CANDIDATES:
                    return

        path_a_codes = [type_a] + [type_a + adj for adj in HEXAGON_ADJACENT.get(type_a, [])]
        path_b_codes = [type_b] + [type_b + adj for adj in HEXAGON_ADJACENT.get(type_b, [])]

        _add_from_codes(path_a_codes, "A")
        expansion_summary["path_a_count"] = sum(
            1 for c in display_candidates + backup_candidates if c.get("path") == "A"
        )
        _add_from_codes(path_b_codes, "B")
        expansion_summary["path_b_count"] = sum(
            1 for c in display_candidates + backup_candidates if c.get("path") == "B"
        )

        all_candidates = display_candidates + backup_candidates
        expansion_summary["display_count"] = len(display_candidates)
        expansion_summary["backup_count"]  = len(backup_candidates)
        expansion_summary["total_unique"]  = len(seen)

        return {
            "user_riasec_code":        riasec_code,
            "user_top_3_types":        top_3_types,
            "user_scores":             user_scores,
            "is_inconsistent_profile": True,
            "candidates":              all_candidates,
            "expansion_summary":       expansion_summary,
        }

    # ─────────────────────────────────────────────────────────────────
    # PRIVATE HELPERS — Query
    # ─────────────────────────────────────────────────────────────────

    def _query_by_code_id(
        self, riasec_code_id: int, seen: Set[int], limit: int
    ) -> List[Profession]:
        profs = self.profession_repo.get_professions_by_riasec_code_id(
            riasec_code_id, limit=limit + len(seen)
        )
        result = []
        for p in profs:
            if p.id not in seen:
                seen.add(p.id)
                result.append(p)
                if len(result) >= limit:
                    break
        return result

    def _query_by_code_string(
        self, code_str: str, seen: Set[int], limit: int
    ) -> List[Profession]:
        try:
            code_obj = self.riasec_repo.get_riasec_code_by_string(code_str)
        except HTTPException:
            return []
        return self._query_by_code_id(code_obj.id, seen, limit)

    def _query_by_code_strings(
        self, code_strings: List[str], seen: Set[int], limit: int
    ) -> List[Profession]:
        results: List[Profession] = []
        for code_str in code_strings:
            if len(results) >= limit:
                break
            batch = self._query_by_code_string(code_str, seen, limit - len(results))
            results.extend(batch)
        return results

    # ─────────────────────────────────────────────────────────────────
    # PRIVATE HELPERS — Code Generation
    # ─────────────────────────────────────────────────────────────────

    def _generate_congruent_codes(self, user_code: str, top_3: List[str]) -> List[str]:
        """Semua permutasi 3 huruf top, kecuali kode user sendiri."""
        all_perms = [''.join(p) for p in permutations(top_3)]
        return [c for c in all_perms if c != user_code]

    def _generate_subset_codes(self, top_3: List[str]) -> List[str]:
        """Semua permutasi 2 huruf dari top 3."""
        codes = []
        for i in range(len(top_3)):
            for j in range(len(top_3)):
                if i != j:
                    codes.append(top_3[i] + top_3[j])
        return codes

    # ─────────────────────────────────────────────────────────────────
    # PRIVATE HELPERS — Entry Builder
    # ─────────────────────────────────────────────────────────────────

    def _make_entry(
        self,
        prof: Profession,
        riasec_code_id: int,
        tier,
        congruence_type: str,
        congruence_score: float,
        display_order: int,
        is_display: bool,
        extra: Dict = None,
    ) -> Dict[str, Any]:
        entry = {
            "profession_id":       prof.id,
            "riasec_code_id":      riasec_code_id,
            "expansion_tier":      tier,
            "congruence_type":     congruence_type,
            "congruence_score":    congruence_score,
            "display_order":       display_order,
            "is_display_candidate": is_display,
        }
        if extra:
            entry.update(extra)
        return entry

    # ─────────────────────────────────────────────────────────────────
    # PUBLIC: get_candidates_with_details
    # ─────────────────────────────────────────────────────────────────

    def get_candidates_with_details(self, test_session_id: int) -> Dict[str, Any]:
        """
        Ambil kandidat dari DB + enrich dengan nama profesi.
        Digunakan oleh IkigaiService._generate_ikigai_content().
        """
        candidates_obj = self.profession_repo.get_candidates_by_session_id(test_session_id)
        if not candidates_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidates not found for session {test_session_id}",
            )

        candidates_data = candidates_obj.candidates_data
        profession_ids = [c["profession_id"] for c in candidates_data.get("candidates", [])]
        professions = self.db.query(Profession).filter(
            Profession.id.in_(profession_ids)
        ).all()
        prof_map = {p.id: p for p in professions}

        enriched = []
        for c in candidates_data.get("candidates", []):
            prof = prof_map.get(c["profession_id"])
            if prof:
                enriched.append({
                    **c,
                    "profession_name":        prof.name,
                    "profession_description": prof.about_description,
                    "riasec_code_id":         prof.riasec_code_id,
                })

        return {
            "user_riasec_code":  candidates_data.get("user_riasec_code"),
            "user_top_3_types":  candidates_data.get("user_top_3_types"),
            "user_scores":       candidates_data.get("user_scores"),
            "expansion_summary": candidates_data.get("expansion_summary"),
            "candidates":        enriched,
        }

    # ─────────────────────────────────────────────────────────────────
    # PUBLIC: save_candidates
    # ─────────────────────────────────────────────────────────────────

    def save_candidates(
        self,
        test_session_id: int,
        riasec_code: str,
        riasec_code_id: int,
        user_scores: Dict[str, int],
    ) -> IkigaiCandidateProfession:
        candidates_data = self.expand_candidates(
            riasec_code, riasec_code_id, user_scores
        )
        total = candidates_data["expansion_summary"]["total_unique"]

        existing = self.profession_repo.get_candidates_by_session_id(test_session_id)
        if existing:
            return self.profession_repo.update_candidates(test_session_id, candidates_data)
        else:
            return self.profession_repo.create_candidates(
                test_session_id=test_session_id,
                candidates_data=candidates_data,
                total_candidates=total,
                generation_strategy="tiered_expansion_v2",
                max_candidates_limit=MAX_TOTAL_CANDIDATES,
            )
