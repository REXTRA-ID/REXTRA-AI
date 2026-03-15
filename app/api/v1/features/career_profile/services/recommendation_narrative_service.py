# app/api/v1/categories/career_profile/services/recommendation_narrative_service.py
"""
RecommendationNarrativeService — Generate 6 narasi rekomendasi via Gemini.
"""
import structlog
from app.api.v1.features.career_profile.services.ai_service import career_profile_ai_service

logger = structlog.get_logger()

class RecommendationNarrativeService:
    async def generate_recommendations_narrative(
        self,
        ikigai_responses: dict,       # reasoning_text dari 4 dimensi
        top_2_professions: list,      # data dari ikigai_total_scores
        profession_details: list,     # nama + deskripsi + aktivitas tiap profesi
        user_riasec_code: str,
    ) -> dict:
        """
        1 Gemini call untuk generate semua 6 narasi sekaligus.
        Mendelegasikan ke CareerProfileAIService yang menggunakan PromptManager.
        """
        try:
            return await career_profile_ai_service.generate_recommendation_narrative(
                user_riasec_code=user_riasec_code,
                ikigai_responses=ikigai_responses,
                top_2_professions=top_2_professions,
                profession_details=profession_details
            )
        except Exception as e:
            logger.error("recommendation_narrative_generation_failed", error=str(e))
            return self._get_fallback_narrative(top_2_professions)

    def _get_fallback_narrative(self, top_2_professions: list) -> dict:
        fallback = {
            "ikigai_profile_summary": {
                "what_you_love": (
                    "Kamu memiliki passion kuat pada mengeksplorasi minat dari aktivitas "
                    "yang digemari secara bebas."
                ),
                "what_you_are_good_at": (
                    "Kamu menguasai berbagai keterampilan yang mendukung pencapaian "
                    "pekerjaan berbasis analitis maupun praktis."
                ),
                "what_the_world_needs": (
                    "Sosok dengan impian mengubah lingkungan menjadi positif sangat dibutuhkan "
                    "oleh berbagai komunitas global."
                ),
                "what_you_can_be_paid_for": (
                    "Dedikasimu dalam memberikan yang terbaik bisa diapresiasi dengan sangat "
                    "bernilai dalam industri yang relevan."
                ),
            },
            "match_reasoning": {},
        }
        for prof in top_2_professions:
            pid = str(prof["profession_id"])
            fallback["match_reasoning"][pid] = (
                "Profesi ini cocok karena melibatkan keahlian teknis yang sinkron dengan minat kamu. "
                "Kamu akan menemukan pengalaman berkembang yang cepat di lingkungan kerja kolaboratif ini."
            )
        return fallback
