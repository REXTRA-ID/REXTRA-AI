# app/api/v1/categories/career_profile/services/ai_content_service.py
"""
AIContentService — Wrapper Gemini untuk generate konten dimensi Ikigai.

Sesuai spesifikasi:
    Brief Ikigai Part 1, Bagian 8:
    "ai_content_service.py — Wrapper Gemini API: batch generate + fallback"

Service ini bertanggung jawab untuk:
1. Menerima konteks profesi kandidat (output dari ProfessionDataService)
2. Memanggil Gemini via GeminiFlashClient.generate_ikigai_content() — 1 batch call
3. Retry 1x jika Gemini gagal
4. Fallback statis jika masih gagal setelah retry
5. Return: list narasi + opsi per dimensi per profesi

Output per profesi:
    - what_you_love, what_you_are_good_at,
      what_the_world_needs, what_you_can_be_paid_for  → narasi 2 kalimat (info card)
    - *_option (4 field)                               → teks 1 kalimat (checkbox soal Flutter)

Implementasi Gemini call aktual ada di shared/ai_client.py (GeminiFlashClient.generate_ikigai_content).
"""

import logging
from typing import List, Dict, Any

from app.shared.ai_client import gemini_client
from app.api.v1.kenali_diri.career_profile.prompts.ikigai_prompts import FALLBACK_CONTENT_TEMPLATE

logger = logging.getLogger(__name__)


class AIContentService:
    """
    Wrapper untuk generate konten dimensi Ikigai via Gemini.

    Alur:
    1. Terima konteks profesi kandidat (max 5 profesi display)
    2. Kirim 1 Gemini call batch untuk semua profesi sekaligus
    3. Jika gagal → retry 1x
    4. Jika masih gagal → return fallback statis
    """

    async def generate_dimension_content(
        self, profession_contexts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate narasi + opsi checkbox 4 dimensi Ikigai untuk setiap profesi secara batch.

        Args:
            profession_contexts: List dict konteks profesi dari ProfessionDataService.
                                  Setiap item harus memiliki:
                                  profession_id, name, activities, hard_skills_required, dll.

        Returns:
            List dict, satu item per profesi, masing-masing berisi:
            {
                "profession_id": int,
                "what_you_love": str,            # narasi 2 kalimat (info card)
                "what_you_are_good_at": str,
                "what_the_world_needs": str,
                "what_you_can_be_paid_for": str,
                "what_you_love_option": str,     # teks 1 kalimat (checkbox soal)
                "what_you_are_good_at_option": str,
                "what_the_world_needs_option": str,
                "what_you_can_be_paid_for_option": str
            }
        """
        if not profession_contexts:
            logger.warning("ai_content_service: profession_contexts kosong")
            return []

        # Attempt 1
        try:
            result = await gemini_client.generate_ikigai_content(profession_contexts)
            if result and len(result) > 0:
                logger.info(
                    "ai_content_service: content generated successfully",
                    profession_count=len(result),
                )
                return result
        except Exception as e:
            logger.warning(
                "ai_content_service: attempt 1 failed, retrying",
                error=str(e),
            )

        # Attempt 2 — retry 1x
        try:
            result = await gemini_client.generate_ikigai_content(profession_contexts)
            if result and len(result) > 0:
                logger.info(
                    "ai_content_service: content generated on retry",
                    profession_count=len(result),
                )
                return result
        except Exception as e:
            logger.error(
                "ai_content_service: retry also failed, using fallback",
                error=str(e),
            )

        # Fallback statis
        logger.warning(
            "ai_content_service: using static fallback",
            profession_count=len(profession_contexts),
        )
        return self.get_fallback_content(profession_contexts)

    def get_fallback_content(
        self, profession_contexts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Konten fallback statis jika Gemini gagal setelah 1 retry.
        Template dari ikigai_prompts.FALLBACK_CONTENT_TEMPLATE.

        Args:
            profession_contexts: List dict konteks profesi

        Returns:
            List dict konten fallback, format sama dengan generate_dimension_content()
        """
        return [
            {
                "profession_id": prof["profession_id"],
                "what_you_love": FALLBACK_CONTENT_TEMPLATE["what_you_love"],
                "what_you_are_good_at": FALLBACK_CONTENT_TEMPLATE["what_you_are_good_at"].format(
                    skills=", ".join(
                        (prof.get("hard_skills_required") or [])[:3]
                    ) or "skill teknis relevan"
                ),
                "what_the_world_needs": FALLBACK_CONTENT_TEMPLATE["what_the_world_needs"],
                "what_you_can_be_paid_for": FALLBACK_CONTENT_TEMPLATE["what_you_can_be_paid_for"],
                # Opsi checkbox fallback (poin 13)
                "what_you_love_option":            FALLBACK_CONTENT_TEMPLATE["what_you_love_option"],
                "what_you_are_good_at_option":     FALLBACK_CONTENT_TEMPLATE["what_you_are_good_at_option"],
                "what_the_world_needs_option":     FALLBACK_CONTENT_TEMPLATE["what_the_world_needs_option"],
                "what_you_can_be_paid_for_option": FALLBACK_CONTENT_TEMPLATE["what_you_can_be_paid_for_option"],
            }
            for prof in profession_contexts
        ]


# Singleton instance — gunakan ini di IkigaiService
ai_content_service = AIContentService()
