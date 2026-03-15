# app/api/v1/categories/career_profile/services/ikigai_service.py

import asyncio
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import time

from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from fastapi import HTTPException, status
import structlog

from app.api.v1.features.career_profile.repositories.session_repo import SessionRepository
from app.api.v1.features.career_profile.repositories.profession_repo import ProfessionRepository
from app.api.v1.features.career_profile.services.profession_expansion import ProfessionExpansionService
from app.api.v1.features.career_profile.models.ikigai import (
    IkigaiResponse,
    IkigaiDimensionScores,
    IkigaiTotalScores,
    IkigaiCandidateProfession,
)
from app.api.v1.features.career_profile.schemas.ikigai import (
    IkigaiContentResponse,
    DimensionContent,
    CandidateWithContent,
    DimensionSubmitResponse,
    IkigaiCompletionResponse,
    ProfessionScoreBreakdown,
)
from app.db.models.user import User
from app.api.v1.features.career_profile.services.ai_service import career_profile_ai_service
from app.shared.cache import redis_client, cache_get_raw, cache_set_raw
from app.shared.scoring_utils import (
    calculate_text_score,    # calculate_min_max_normalization DIHAPUS (DEPRECATED)
    calculate_click_score,
    normalize_min_max,
)
from app.api.v1.features.career_profile.services.recommendation_narrative_service import (
    RecommendationNarrativeService,
)
from app.api.v1.features.career_profile.models.result import CareerRecommendation
from app.api.v1.features.career_profile.services.user_career_profile_service import UserCareerProfileService
from app.api.v1.features.career_profile.models.riasec import RIASECResult
from app.models.profession import Profession

logger = structlog.get_logger()

IKIGAI_DIMENSIONS = [
    "what_you_love",
    "what_you_are_good_at",
    "what_the_world_needs",
    "what_you_can_be_paid_for",
]


class IkigaiService:
    def __init__(self, db: Session):
        self.db = db
        self.session_repo = SessionRepository(db)
        self.profession_repo = ProfessionRepository(db)
        self.expansion_service = ProfessionExpansionService(db)

    # --------------------------------------------------------------------------
    # PHASE 1: GENERATE CONTENT
    # --------------------------------------------------------------------------

    async def start_ikigai_session(
        self, user: User, session_token: str
    ) -> IkigaiContentResponse:
        session = self.session_repo.get_by_token(self.db, session_token)
        if not session or session.user_id != user.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")

        # === PERBAIKAN TEMUAN 2: Validasi uses_ikigai dan test_goal ===
        if not session.uses_ikigai:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Sesi ini adalah FIT_CHECK — tidak memiliki alur Ikigai",
            )
        if session.test_goal != "RECOMMENDATION":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Hanya sesi RECOMMENDATION yang bisa masuk ke fase Ikigai",
            )

        if session.status not in ["riasec_completed", "ikigai_ongoing"]:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Status sesi tidak valid untuk memulai Ikigai: {session.status}",
            )

        if session.status == "riasec_completed":
            session.status = "ikigai_ongoing"

            # === PERBAIKAN TEMUAN 1: INSERT placeholder IkigaiResponse dalam transaksi yang sama ===
            # Menjamin setiap sesi ikigai_ongoing selalu punya baris di ikigai_responses.
            # Kolom dimensi dibiarkan NULL — diisi bertahap via submit_dimension.
            placeholder = IkigaiResponse(test_session_id=session.id)
            self.db.add(placeholder)
            self.db.commit()

        # Cek Redis cache
        cache_key = f"ikigai:content:{session_token}"
        cached_raw = cache_get_raw(cache_key)   # graceful — None jika Redis down atau miss
        if cached_raw:
            try:
                content = json.loads(cached_raw)
                return IkigaiContentResponse(
                    session_token=session_token,
                    status="ikigai_ongoing",
                    generated_at=content["generated_at"],
                    from_cache=True,
                    regenerated=False,
                    total_display_candidates=len(content["candidates"]),
                    message="Konten Ikigai diambil dari cache.",
                    candidates_with_content=content["candidates"],
                )
            except (json.JSONDecodeError, KeyError):
                pass  # Cache corrupt — lanjut generate ulang

        # Generate konten baru
        candidates = await self._generate_ikigai_content(session.id)
        now_str = datetime.now(timezone.utc).isoformat()
        cache_payload = {"generated_at": now_str, "candidates": candidates}
        cache_set_raw(cache_key, json.dumps(cache_payload), ttl=7200)  # graceful

        expansion_meta = self._get_expansion_metadata(session.id)
        return IkigaiContentResponse(
            session_token=session_token,
            status="ikigai_ongoing",
            generated_at=now_str,
            from_cache=False,
            regenerated=True,
            total_display_candidates=len(candidates),
            total_backup_candidates=expansion_meta.get("backup_count", 0),
            total_all_candidates=expansion_meta.get("total_count", len(candidates)),
            user_riasec_code=expansion_meta.get("user_riasec_code", ""),
            congruent_codes_used=expansion_meta.get("congruent_codes_used", []),
            expansion_summary=expansion_meta.get("expansion_summary"),
            backup_candidates=expansion_meta.get("backup_candidates", []),
            message="Sesi dimulai dan konten Ikigai berhasil di-generate.",
            candidates_with_content=candidates,
        )

    async def get_ikigai_content(
        self, user: User, session_token: str
    ) -> IkigaiContentResponse:
        session = self.session_repo.get_by_token(self.db, session_token)
        if not session or session.user_id != user.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")

        # === PERBAIKAN TEMUAN 2: Validasi uses_ikigai dan test_goal ===
        if not session.uses_ikigai:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Sesi ini adalah FIT_CHECK — tidak memiliki alur Ikigai",
            )
        if session.test_goal != "RECOMMENDATION":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Hanya sesi RECOMMENDATION yang bisa mengakses konten Ikigai",
            )

        if session.status != "ikigai_ongoing":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Sesi Ikigai tidak dalam status ongoing",
            )

        cache_key = f"ikigai:content:{session_token}"
        cached_raw = cache_get_raw(cache_key)
        if cached_raw:
            try:
                content = json.loads(cached_raw)
                return IkigaiContentResponse(
                    session_token=session_token,
                    status="ikigai_ongoing",
                    generated_at=content["generated_at"],
                    from_cache=True,
                    regenerated=False,
                    total_display_candidates=len(content["candidates"]),
                    message="Berhasil mengambil konten Ikigai dari cache.",
                    candidates_with_content=content["candidates"],
                )
            except (json.JSONDecodeError, KeyError):
                pass

        # Cache miss atau corrupt — regenerate
        candidates = await self._generate_ikigai_content(session.id)
        now_str = datetime.now(timezone.utc).isoformat()
        cache_payload = {"generated_at": now_str, "candidates": candidates}
        cache_set_raw(cache_key, json.dumps(cache_payload), ttl=7200)

        return IkigaiContentResponse(
            session_token=session_token,
            status="ikigai_ongoing",
            generated_at=now_str,
            from_cache=False,
            regenerated=True,
            total_display_candidates=len(candidates),
            message="Konten lama expired, regenerasi berhasil.",
            candidates_with_content=candidates,
        )

    def _get_expansion_metadata(self, session_id: int) -> dict:
        """Ambil metadata ekspansi kandidat dari DB untuk ditampilkan di response."""
        try:
            candidate_record = (
                self.db.query(IkigaiCandidateProfession)
                .filter(IkigaiCandidateProfession.test_session_id == session_id)
                .first()
            )
            if not candidate_record or not candidate_record.candidates_data:
                return {}
            all_cands = candidate_record.candidates_data.get("candidates", [])
            meta      = candidate_record.candidates_data.get("metadata", {})
            display   = [c for c in all_cands if c.get("is_display_candidate",
                         c.get("display_order", 99) <= 5)]
            backup    = [c for c in all_cands if not c.get("is_display_candidate",
                         c.get("display_order", 99) <= 5)]
            exp_summary = meta.get("expansion_summary", {})
            backup_list = [
                {"profession_id": c["profession_id"], "name": "",
                 "congruence_type": c.get("congruence_type", ""),
                 "expansion_tier":  c.get("expansion_tier")}
                for c in backup
            ]
            return {
                "backup_count":         len(backup),
                "total_count":          len(all_cands),
                "user_riasec_code":     meta.get("user_riasec_code", ""),
                "congruent_codes_used": [],
                "expansion_summary":    exp_summary,
                "backup_candidates":    backup_list,
            }
        except Exception:
            return {}

    async def _generate_ikigai_content(self, session_id: int) -> List[Dict]:
        """
        Generate narasi konten Ikigai untuk kandidat display (display_order 1–5).
        Menggunakan ProfessionRepository untuk query relasional ke tabel professions.
        """
        candidates_data = self.expansion_service.get_candidates_with_details(session_id)
        top_candidates = [
            c for c in candidates_data["candidates"] if c.get("display_order", 99) <= 5
        ]

        top_profession_ids = [c["profession_id"] for c in top_candidates]

        # Query via ProfessionRepository — tabel relasional (bukan DigitalProfession)
        profession_contexts = self.profession_repo.get_profession_contexts_for_ikigai(
            top_profession_ids
        )
        prof_context_map = {pc["profession_id"]: pc for pc in profession_contexts}

        ai_responses = await career_profile_ai_service.generate_ikigai_content(profession_contexts)
        # Normalisasi key ke int — Gemini kadang return profession_id sebagai string
        ai_map = {
            int(item["profession_id"]): item
            for item in ai_responses
            if "profession_id" in item
        }

        result_candidates = []
        for c in top_candidates:
            pid = c["profession_id"]
            pc = prof_context_map.get(pid, {})
            ai_data = ai_map.get(pid, {})

            result_candidates.append({
                "profession_id": pid,
                "profession_name": pc.get("name", c.get("profession_name", "Unknown")),
                "display_order": c.get("display_order", 0),
                "congruence_score": c.get("congruence_score", 0.5),
                "dimension_content": {
                    "what_you_love": ai_data.get("what_you_love", "Deskripsi tidak tersedia."),
                    "what_you_are_good_at": ai_data.get("what_you_are_good_at", "Deskripsi tidak tersedia."),
                    "what_the_world_needs": ai_data.get("what_the_world_needs", "Deskripsi tidak tersedia."),
                    "what_you_can_be_paid_for": ai_data.get("what_you_can_be_paid_for", "Deskripsi tidak tersedia."),
                },
            })

        return result_candidates

    # --------------------------------------------------------------------------
    # PHASE 2: SUBMIT DIMENSI
    # --------------------------------------------------------------------------

    async def submit_dimension(
        self,
        user: User,
        session_token: str,
        dimension_name: str,
        selected_profession_ids: list = None,    # POIN 14: plural list
        selected_profession_id:  int = None,     # backward compat
        selection_type: str = "not_selected",
        reasoning_text: str = "",
    ):
        # Normalisasi: pakai plural jika ada, fallback ke singular
        if selected_profession_ids is None:
            selected_profession_ids = [selected_profession_id] if selected_profession_id else []
        # Ambil ID pertama untuk logika lama yang butuh singular
        selected_profession_id = selected_profession_ids[0] if selected_profession_ids else None
        session = self.session_repo.get_by_token(self.db, session_token)
        if not session or session.user_id != user.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")

        if session.status != "ikigai_ongoing":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Sesi tidak bisa di-submit (bukan ikigai_ongoing)",
            )

        ikigai_resp = (
            self.db.query(IkigaiResponse)
            .filter(IkigaiResponse.test_session_id == session.id)
            .first()
        )
        if not ikigai_resp:
            # Seharusnya sudah ada sejak /start — tapi defensif jika tidak ada
            ikigai_resp = IkigaiResponse(test_session_id=session.id)
            self.db.add(ikigai_resp)
            self.db.flush()

        # === PERBAIKAN TEMUAN 4: Cek apakah dimensi sudah dijawab sebelumnya ===
        dim_field_map = {
            "what_you_love":          "dimension_1_love",
            "what_you_are_good_at":   "dimension_2_good_at",
            "what_the_world_needs":   "dimension_3_world_needs",
            "what_you_can_be_paid_for": "dimension_4_paid_for",
        }
        field_name = dim_field_map[dimension_name]
        existing_value = getattr(ikigai_resp, field_name)
        if existing_value is not None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Dimensi '{dimension_name}' sudah dijawab sebelumnya dan tidak bisa diubah.",
            )

        # === PERBAIKAN TEMUAN 5: Validasi selected_profession_id terhadap kandidat sesi ===
        if selected_profession_id is not None:
            candidate_record = (
                self.db.query(IkigaiCandidateProfession)
                .filter(IkigaiCandidateProfession.test_session_id == session.id)
                .first()
            )
            valid_ids = set()
            if candidate_record and candidate_record.candidates_data:
                valid_ids = {
                    c["profession_id"]
                    for c in candidate_record.candidates_data.get("candidates", [])
                }
            if selected_profession_id not in valid_ids:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    f"selected_profession_id {selected_profession_id} "
                    f"bukan bagian dari kandidat profesi untuk sesi ini.",
                )

        dim_data = {
            "selected_profession_id": selected_profession_id,
            "selection_type": selection_type,
            "reasoning_text": reasoning_text,
            "answered_at": datetime.now(timezone.utc).isoformat(),
        }

        setattr(ikigai_resp, field_name, dim_data)
        flag_modified(ikigai_resp, field_name)
        self.db.commit()

        # Cek kelengkapan dimensi
        completed_dims = []
        if ikigai_resp.dimension_1_love:        completed_dims.append("what_you_love")
        if ikigai_resp.dimension_2_good_at:     completed_dims.append("what_you_are_good_at")
        if ikigai_resp.dimension_3_world_needs: completed_dims.append("what_the_world_needs")
        if ikigai_resp.dimension_4_paid_for:    completed_dims.append("what_you_can_be_paid_for")

        remaining = [d for d in IKIGAI_DIMENSIONS if d not in completed_dims]
        all_completed = len(remaining) == 0

        if not all_completed:
            return DimensionSubmitResponse(
                session_token=session_token,
                dimension_saved=dimension_name,
                dimensions_completed=completed_dims,
                dimensions_remaining=remaining,
                all_completed=False,
                message=f"Dimensi '{dimension_name}' berhasil disimpan.",
            )

        # Semua 4 dimensi selesai → trigger scoring pipeline
        try:
            result = await self._finalize_ikigai(session, ikigai_resp)
            return result
        except HTTPException:
            raise
        except Exception as e:
            logger.error("ikigai_finalize_failed", error=str(e), session_id=session.id)
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Gagal menghitung skor final: {str(e)}",
            )

    # --------------------------------------------------------------------------
    # PHASE 2 INTERNAL: SCORING PIPELINE
    # --------------------------------------------------------------------------

    async def _finalize_ikigai(self, session, ikigai_resp: IkigaiResponse):
        """
        Pipeline scoring Ikigai sesuai Brief Part 2.

        STEP 1 : Ambil semua kandidat dari DB
        STEP 2 : Kumpulkan jawaban user
        STEP 3 : 4 Gemini call paralel (1 per dimensi)
        STEP 4 : Normalisasi min-max + hitung text_score & click_score
        STEP 5 : Deteksi tie SEBELUM sort → simpan di tie_info
        STEP 6 : Sort multi-level + assign rank ke setiap entri
        STEP 7 : INSERT ikigai_dimension_scores (metadata lengkap)
        STEP 8 : INSERT ikigai_total_scores (rank di JSONB + metadata lengkap)
        STEP 9 : Update status sesi + kenalidiri_history
        STEP 10: Generate narasi rekomendasi (best-effort, non-fatal)
        """
        start_time = time.time()

        # ------------------------------------------------------------------
        # STEP 1: Ambil semua kandidat dari DB
        # ------------------------------------------------------------------
        candidate_record = self.profession_repo.get_candidates_by_session_id(session.id)
        if not candidate_record or not candidate_record.candidates_data:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Data kandidat profesi tidak ditemukan untuk sesi ini.",
            )
        all_candidate_entries = candidate_record.candidates_data.get("candidates", [])
        all_profession_ids = [c["profession_id"] for c in all_candidate_entries]

        # Query profesi via tabel relasional (bukan DigitalProfession)
        profession_contexts = self.profession_repo.get_profession_contexts_for_scoring(
            all_profession_ids
        )
        prof_context_map = {pc["profession_id"]: pc for pc in profession_contexts}

        if not profession_contexts:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Tidak ada profesi valid yang bisa di-scoring.",
            )

        # ------------------------------------------------------------------
        # STEP 2: Kumpulkan jawaban user
        # ------------------------------------------------------------------
        answers = {
            "what_you_love":            ikigai_resp.dimension_1_love,
            "what_you_are_good_at":     ikigai_resp.dimension_2_good_at,
            "what_the_world_needs":     ikigai_resp.dimension_3_world_needs,
            "what_you_can_be_paid_for": ikigai_resp.dimension_4_paid_for,
        }

        valid_profession_id_set = {pc["profession_id"] for pc in profession_contexts}
        selected_ids: Dict[str, Optional[int]] = {}
        for dim, ans in answers.items():
            if not ans:
                selected_ids[dim] = None
                continue
            sel_id = ans.get("selected_profession_id")
            if sel_id and sel_id not in valid_profession_id_set:
                logger.warning(
                    "ikigai_invalid_selected_profession",
                    dimension=dim,
                    selected_profession_id=sel_id,
                    session_id=session.id,
                )
                selected_ids[dim] = None
            else:
                selected_ids[dim] = sel_id

        # ------------------------------------------------------------------
        # STEP 3: 4 Gemini call paralel (1 per dimensi, semua kandidat)
        # ------------------------------------------------------------------
        scoring_tasks = []
        dim_order = []
        for dim in IKIGAI_DIMENSIONS:
            ans = answers.get(dim)
            if not ans:
                continue
            reasoning_text = ans.get("reasoning_text", "").strip() or "(tidak ada teks jawaban)"
            scoring_tasks.append(
                career_profile_ai_service.score_ikigai_batch(
                    dimension_name=dim,
                    user_reasoning_text=reasoning_text,
                    profession_contexts=profession_contexts,
                )
            )
            dim_order.append(dim)

        logger.info(
            "ikigai_scoring_start",
            session_id=session.id,
            dimensions=dim_order,
            total_professions=len(profession_contexts),
        )
        gemini_results = await asyncio.gather(*scoring_tasks, return_exceptions=True)

        # ------------------------------------------------------------------
        # STEP 4: Normalisasi min-max + text_score & click_score
        # ------------------------------------------------------------------
        # Catat dimensi yang gagal untuk metadata
        failed_dimensions: List[str] = []
        fallback_used = False

        dim_raw_scores: Dict[str, list] = {}
        for dim, result in zip(dim_order, gemini_results):
            if isinstance(result, Exception):
                logger.error(
                    "ikigai_scoring_dim_failed",
                    dimension=dim,
                    error=str(result),
                    session_id=session.id,
                )
                failed_dimensions.append(dim)
                fallback_used = True
                # Fallback: semua profesi r_raw = 0.5
                dim_raw_scores[dim] = [
                    {"profession_id": pc["profession_id"], "r_raw": 0.5}
                    for pc in profession_contexts
                ]
            else:
                dim_raw_scores[dim] = result

        # Normalisasi min-max per dimensi
        dim_scored: Dict[str, list] = {}
        normalization_params: Dict[str, dict] = {}

        for dim in dim_order:
            raw_list = dim_raw_scores[dim]
            r_values = [item["r_raw"] for item in raw_list]
            r_min = min(r_values) if r_values else 0.0
            r_max = max(r_values) if r_values else 1.0
            denom = r_max - r_min

            normalization_params[dim] = {
                "r_min": round(r_min, 4),
                "r_max": round(r_max, 4),
                "professions_evaluated": len(raw_list),
            }

            sel_id_for_dim = selected_ids.get(dim)
            scored_list = []
            for item in raw_list:
                r_raw = item["r_raw"]
                # Gunakan utility function baru (termasuk penanganan denom=0)
                r_norm = normalize_min_max(r_raw, r_min, r_max)

                is_selected = (
                    sel_id_for_dim is not None
                    and item["profession_id"] == sel_id_for_dim
                )
                t_score = calculate_text_score(r_norm)           # 0.0–15.0
                c_score = calculate_click_score(r_raw, is_selected)  # 0.0–10.0

                scored_list.append({
                    "profession_id": item["profession_id"],
                    "r_raw": round(r_raw, 4),
                    "r_normalized": r_norm,
                    "text_score": t_score,
                    "click_score": c_score,
                    "dimension_total": round(t_score + c_score, 4),
                })
            dim_scored[dim] = scored_list

        # ------------------------------------------------------------------
        # STEP 5: Agregasi total_score per profesi
        # ------------------------------------------------------------------
        congruence_map = {
            c["profession_id"]: c.get("congruence_score", 0.5)
            for c in all_candidate_entries
        }
        dim_score_by_pid: Dict[str, Dict[int, dict]] = {
            dim: {item["profession_id"]: item for item in scored_list}
            for dim, scored_list in dim_scored.items()
        }

        total_scores = []
        for pid in all_profession_ids:
            score_per_dim: Dict[str, float] = {}
            sum_r_normalized = 0.0
            scored_dim_count = 0

            for dim in IKIGAI_DIMENSIONS:
                if dim in dim_score_by_pid and pid in dim_score_by_pid[dim]:
                    entry = dim_score_by_pid[dim][pid]
                    score_per_dim[dim] = entry["dimension_total"]
                    sum_r_normalized += entry["r_normalized"]
                    scored_dim_count += 1
                else:
                    score_per_dim[dim] = 0.0

            total_dim_score = sum(score_per_dim.values())
            intrinsic = score_per_dim.get("what_you_love", 0.0) + score_per_dim.get("what_you_are_good_at", 0.0)
            extrinsic = score_per_dim.get("what_the_world_needs", 0.0) + score_per_dim.get("what_you_can_be_paid_for", 0.0)
            avg_r_norm = sum_r_normalized / scored_dim_count if scored_dim_count > 0 else 0.0
            congruence = congruence_map.get(pid, 0.0)
            pc = prof_context_map.get(pid, {})

            total_scores.append({
                "profession_id": pid,
                "profession_name": pc.get("name", "Unknown"),
                "total_score": round(total_dim_score, 4),
                "intrinsic_score": round(intrinsic, 4),
                "extrinsic_score": round(extrinsic, 4),
                "congruence_score": round(congruence, 4),
                "avg_r_normalized": round(avg_r_norm, 4),
                "score_what_you_love": round(score_per_dim.get("what_you_love", 0.0), 4),
                "score_what_you_are_good_at": round(score_per_dim.get("what_you_are_good_at", 0.0), 4),
                "score_what_the_world_needs": round(score_per_dim.get("what_the_world_needs", 0.0), 4),
                "score_what_you_can_be_paid_for": round(score_per_dim.get("what_you_can_be_paid_for", 0.0), 4),
            })

        # ------------------------------------------------------------------
        # STEP 6 — PERBAIKAN TEMUAN 7: Deteksi tie SEBELUM sort
        # ------------------------------------------------------------------
        # Tie didefinisikan: ada 2 atau lebih profesi dengan total_score yang sama.
        # Deteksi dilakukan sebelum sort agar `tie_breaking_applied` akurat.
        top_score = max((p["total_score"] for p in total_scores), default=0.0)
        tied_professions = [p for p in total_scores if p["total_score"] == top_score]
        tie_breaking_applied = len(tied_professions) > 1

        tie_breaking_details = None
        if tie_breaking_applied:
            tie_breaking_details = {
                "tied_profession_ids": [p["profession_id"] for p in tied_professions],
                "tied_total_score": top_score,
                "tiebreak_criteria_used": ["intrinsic_score", "congruence_score", "avg_r_normalized"],
            }

        # Multi-level tie-breaking: total_score → intrinsic → congruence → avg_r_normalized
        total_scores.sort(
            key=lambda x: (
                x["total_score"],
                x["intrinsic_score"],
                x["congruence_score"],
                x["avg_r_normalized"],
            ),
            reverse=True,
        )

        # === PERBAIKAN TEMUAN 6: Assign rank ke setiap entri SETELAH sort ===
        for rank_idx, p in enumerate(total_scores, start=1):
            p["rank"] = rank_idx

        top_1_id = total_scores[0]["profession_id"] if total_scores else None
        top_2_id = total_scores[1]["profession_id"] if len(total_scores) > 1 else None
        calculated_at = datetime.now(timezone.utc).isoformat()

        # ------------------------------------------------------------------
        # STEP 7 — PERBAIKAN TEMUAN 9: INSERT ikigai_dimension_scores (metadata lengkap)
        # ------------------------------------------------------------------
        dimension_scores_jsonb = {
            "dimension_scores": dim_scored,
            "normalization_params": normalization_params,
            "metadata": {
                "total_candidates_scored": len(profession_contexts),   # nama sesuai brief
                "scoring_strategy": "batch_semantic_matching",         # nilai sesuai brief
                "fallback_used": fallback_used,                        # baru
                "failed_dimensions": failed_dimensions,                # baru
                "calculated_at": calculated_at,                        # baru
            },
        }

        dim_score_db = IkigaiDimensionScores(
            test_session_id=session.id,
            scores_data=dimension_scores_jsonb,
            ai_model_used="gemini-1.5-flash",
            total_api_calls=len(dim_order),
        )
        self.db.add(dim_score_db)

        # ------------------------------------------------------------------
        # STEP 8 — PERBAIKAN TEMUAN 6, 8: INSERT ikigai_total_scores (rank + metadata lengkap)
        # ------------------------------------------------------------------
        total_scores_jsonb = {
            "profession_scores": total_scores,   # setiap item sudah punya field "rank"
            "metadata": {
                "total_professions_ranked": len(total_scores),
                "tie_breaking_applied": tie_breaking_applied,
                "tie_breaking_details": tie_breaking_details,          # baru
                "top_2_professions": [top_1_id, top_2_id],            # baru
                "calculated_at": calculated_at,                        # baru
            },
        }

        tot_score_db = IkigaiTotalScores(
            test_session_id=session.id,
            scores_data=total_scores_jsonb,
            top_profession_1_id=top_1_id,
            top_profession_2_id=top_2_id,
        )
        self.db.add(tot_score_db)

        # ------------------------------------------------------------------
        # STEP 9: Update status sesi & kenalidiri_history
        # ------------------------------------------------------------------
        ikigai_resp.completed = True
        ikigai_resp.completed_at = datetime.now(timezone.utc)

        session.status = "completed"
        session.ikigai_completed_at = datetime.now(timezone.utc)
        session.completed_at = datetime.now(timezone.utc)

        from app.db.models.kenalidiri_history import KenaliDiriHistory
        history = (
            self.db.query(KenaliDiriHistory)
            .filter(KenaliDiriHistory.detail_session_id == session.id)
            .first()
        )
        if history:
            history.status = "completed"
            history.completed_at = datetime.now(timezone.utc)

        # ── AUTO-SAVE user_career_profiles (tes RECOMMENDATION pertama) ──────
        try:
            # Ambil ID dari hasil rekomendasi yang baru saja dibuat
            _ucp_svc = UserCareerProfileService(self.db)
            _ucp_svc.auto_save_if_first(
                user_id=session.user_id,
                session=session,
                top_profession1_id=top_1_id,
                top_profession2_id=top_2_id,
                riasec_code=user_riasec_code,
            )
        except Exception as _ucp_err:
            logger.warning("user_career_profile_auto_save_failed", error=str(_ucp_err))

        self.db.commit()

        elapsed = round(time.time() - start_time, 2)
        logger.info(
            "ikigai_finalize_success",
            session_id=session.id,
            total_professions=len(total_scores),
            top_1_id=top_1_id,
            top_2_id=top_2_id,
            tie_breaking_applied=tie_breaking_applied,
            elapsed_seconds=elapsed,
        )

        # ------------------------------------------------------------------
        # STEP 10: Generate narasi rekomendasi (best-effort, non-fatal)
        # ------------------------------------------------------------------
        # Definisikan top_2_scores di luar try agar fallback bisa akses
        top_2_scores = total_scores[:2]
        user_riasec_code = "Unknown"

        # INSERT minimal dulu — pastikan row ada meski narrative gagal
        try:
            _minimal_data = {
                "ikigai_profile_summary": {},
                "recommended_professions": [
                    {"rank": i+1, "profession_id": p["profession_id"],
                     "profession_name": p.get("profession_name", ""),
                     "match_percentage": round(p["total_score"], 2)}
                    for i, p in enumerate(top_2_scores)
                ],
                "generation_context": {"status": "pending_narrative"},
                "points_awarded": None,
            }
            _minimal_rec = CareerRecommendation(
                test_session_id=session.id,
                recommendations_data=_minimal_data,
            )
            self.db.add(_minimal_rec)
            self.db.commit()
            logger.info("recommendation_minimal_saved", session_id=session.id)
        except Exception as _min_err:
            self.db.rollback()
            logger.error("recommendation_minimal_failed", error=str(_min_err))

        try:
            top_2_ids = [p["profession_id"] for p in top_2_scores]

            profession_details = self.profession_repo.get_profession_contexts_for_recommendation(
                top_2_ids
            )

            ikigai_responses_text = {
                dim: (answers.get(dim) or {}).get("reasoning_text", "")
                for dim in IKIGAI_DIMENSIONS
            }

            riasec_res = (
                self.db.query(RIASECResult)
                .filter(RIASECResult.test_session_id == session.id)
                .first()
            )
            # FIX: riasec_code kolom tidak ada di DB, ambil dari riasec_codes table via FK
            if riasec_res:
                from app.api.v1.features.career_profile.models.riasec import RIASECCode
                code_obj = self.db.query(RIASECCode).filter(RIASECCode.id == riasec_res.riasec_code_id).first()
                user_riasec_code = code_obj.riasec_code if code_obj else "Unknown"
            else:
                user_riasec_code = "Unknown"

            # Generate narrative (best-effort, boleh gagal)
            narrative_data = {}
            try:
                narrative_service = RecommendationNarrativeService()
                narrative_data = await narrative_service.generate_recommendations_narrative(
                    ikigai_responses=ikigai_responses_text,
                    top_2_professions=top_2_scores,
                    profession_details=profession_details,
                    user_riasec_code=user_riasec_code,
                )
            except Exception as narr_err:
                logger.warning("narrative_generation_skipped", error=str(narr_err), session_id=session.id)

            recommended_professions = []
            for rank_idx, p in enumerate(top_2_scores, start=1):
                pid = p["profession_id"]
                pc = prof_context_map.get(pid, {})
                reasoning = narrative_data.get("match_reasoning", {}).get(str(pid), "")
                recommended_professions.append({
                    "rank": rank_idx,
                    "profession_id": pid,
                    "profession_name": p.get("profession_name", ""),
                    "match_percentage": round(p["total_score"], 2),
                    "match_reasoning": reasoning,
                    "riasec_alignment": {
                        "user_code": user_riasec_code,
                        "profession_code": pc.get("riasec_code", "-"),
                        "congruence_score": p.get("congruence_score", 0),
                    },
                    "score_breakdown": {
                        "total_score": round(p["total_score"], 2),
                        "intrinsic_score": round(p["intrinsic_score"], 2),
                        "extrinsic_score": round(p["extrinsic_score"], 2),
                        "score_what_you_love": round(p["score_what_you_love"], 2),
                        "score_what_you_are_good_at": round(p["score_what_you_are_good_at"], 2),
                        "score_what_the_world_needs": round(p["score_what_the_world_needs"], 2),
                        "score_what_you_can_be_paid_for": round(p["score_what_you_can_be_paid_for"], 2),
                    },
                })

            recommendations_data = {
                "ikigai_profile_summary": narrative_data.get("ikigai_profile_summary", {}),
                "recommended_professions": recommended_professions,
                "generation_context": {
                    "user_riasec_code": user_riasec_code,
                    "total_candidates_evaluated": len(total_scores),
                    "top_2_selection_method": "total_score_ranking",
                    "generation_timestamp": calculated_at,
                },
                "points_awarded": None,
            }

            # Ambil top 2 profession IDs untuk kolom dedicated
            _top_ids = [
                p["profession_id"]
                for p in recommendations_data.get("recommended_professions", [])
                if p.get("profession_id")
            ]
            _top1_id = _top_ids[0] if len(_top_ids) > 0 else None
            _top2_id = _top_ids[1] if len(_top_ids) > 1 else None

            # UPDATE row career_recommendations yang sudah ada dengan data lengkap
            existing_rec = self.db.query(CareerRecommendation).filter(
                CareerRecommendation.test_session_id == session.id
            ).first()
            if existing_rec:
                existing_rec.recommendations_data  = recommendations_data
                existing_rec.top_profession1_id    = _top1_id   # ← fix NULL
                existing_rec.top_profession2_id    = _top2_id   # ← fix NULL
                flag_modified(existing_rec, "recommendations_data")
            else:
                career_rec = CareerRecommendation(
                    test_session_id=session.id,
                    recommendations_data=recommendations_data,
                    top_profession1_id=_top1_id,
                    top_profession2_id=_top2_id,
                )
                self.db.add(career_rec)
            self.db.commit()
            logger.info("recommendation_saved", session_id=session.id)

        except Exception as e:
            logger.error(
                "recommendation_failed",
                error=str(e),
                session_id=session.id,
            )
            # Fallback: simpan data minimal agar result endpoint tidak 404
            try:
                fallback_data = {
                    "ikigai_profile_summary": {},
                    "recommended_professions": [
                        {"rank": i+1, "profession_id": p["profession_id"],
                         "profession_name": p.get("profession_name", ""),
                         "match_percentage": round(p["total_score"], 2),
                         "match_reasoning": "", "riasec_alignment": {}}
                        for i, p in enumerate(top_2_scores)
                    ],
                    "generation_context": {"user_riasec_code": user_riasec_code},
                    "points_awarded": None,
                }
                fallback_rec = CareerRecommendation(
                    test_session_id=session.id,
                    recommendations_data=fallback_data,
                )
                self.db.add(fallback_rec)
                self.db.commit()
                logger.info("recommendation_fallback_saved", session_id=session.id)
            except Exception as fb_err:
                logger.error("recommendation_fallback_failed", error=str(fb_err))
                self.db.rollback()

        # ------------------------------------------------------------------
        # FORMAT RESPONSE
        # ------------------------------------------------------------------
        breakdown = [
            ProfessionScoreBreakdown(
                rank=p["rank"],
                profession_id=p["profession_id"],
                total_score=round(p["total_score"], 4),
                score_what_you_love=round(p["score_what_you_love"], 4),
                score_what_you_are_good_at=round(p["score_what_you_are_good_at"], 4),
                score_what_the_world_needs=round(p["score_what_the_world_needs"], 4),
                score_what_you_can_be_paid_for=round(p["score_what_you_can_be_paid_for"], 4),
                intrinsic_score=round(p["intrinsic_score"], 4),
                extrinsic_score=round(p["extrinsic_score"], 4),
            )
            for p in total_scores
        ]

        # ── AUTO-SAVE user_career_profiles (AKHIR SESI) ──────
        try:
            _ucp_svc = UserCareerProfileService(self.db)
            _ucp_svc.auto_save_if_first(
                user_id=session.user_id,
                session=session,
                top_profession1_id=top_1_id,
                top_profession2_id=top_2_id,
                riasec_code=user_riasec_code,
            )
        except Exception as _ucp_err:
            logger.warning("user_career_profile_auto_save_failed", error=str(_ucp_err))

        return IkigaiCompletionResponse(
            session_token=session.session_token,
            status="completed",
            top_2_professions=breakdown[:2],
            total_professions_evaluated=len(total_scores),
            tie_breaking_applied=tie_breaking_applied,
            calculated_at=calculated_at,
            message="Ikigai berhasil di-submit dan diskor.",
        )

    # --------------------------------------------------------------------------
    # GET RESULT
    # --------------------------------------------------------------------------

    async def get_ikigai_result(
        self, user: User, session_token: str
    ) -> IkigaiCompletionResponse:
        session = self.session_repo.get_by_token(self.db, session_token)
        if not session or session.user_id != user.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")

        if session.status != "completed":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Ikigai belum selesai."
            )

        total_scores_record = (
            self.db.query(IkigaiTotalScores)
            .filter(IkigaiTotalScores.test_session_id == session.id)
            .first()
        )
        if not total_scores_record:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Result tidak ditemukan.")

        prof_list = total_scores_record.scores_data.get("profession_scores", [])
        metadata = total_scores_record.scores_data.get("metadata", {})

        breakdown = [
            ProfessionScoreBreakdown(
                rank=p.get("rank", idx + 1),   # rank sudah ada di JSONB
                profession_id=p["profession_id"],
                total_score=round(p.get("total_score", 0.0), 4),
                score_what_you_love=round(p.get("score_what_you_love", 0.0), 4),
                score_what_you_are_good_at=round(p.get("score_what_you_are_good_at", 0.0), 4),
                score_what_the_world_needs=round(p.get("score_what_the_world_needs", 0.0), 4),
                score_what_you_can_be_paid_for=round(p.get("score_what_you_can_be_paid_for", 0.0), 4),
                intrinsic_score=round(p.get("intrinsic_score", 0.0), 4),
                extrinsic_score=round(p.get("extrinsic_score", 0.0), 4),
            )
            for idx, p in enumerate(prof_list)
        ]

        return IkigaiCompletionResponse(
            session_token=session.session_token,
            status="completed",
            top_2_professions=breakdown[:2],
            total_professions_evaluated=len(prof_list),
            tie_breaking_applied=metadata.get("tie_breaking_applied", False),
            calculated_at=total_scores_record.calculated_at.isoformat(),
            message="Berhasil mengambil hasil Ikigai.",
        )
