# app/api/v1/categories/career_profile/services/ai_scoring_service.py
"""
AIScoringService — Wrapper Gemini untuk AI scoring relevansi teks per dimensi Ikigai.

Sesuai spesifikasi:
    Brief Ikigai Part 2, Bagian 10:
    "ai_scoring_service.py — AI scoring wrapper: score_single_dimension + score_all_dimensions"

Service ini bertanggung jawab untuk:
1. Menerima teks jawaban user untuk satu dimensi
2. Memanggil Gemini bersama konteks semua profesi kandidat
3. Menerima r_raw (0.0–1.0) per profesi dari Gemini
4. Menangani error per dimensi dengan fallback r_raw = 0.5 (skor netral)
5. Menjalankan scoring 4 dimensi secara paralel via asyncio.gather()

Implementasi Gemini call aktual ada di:
    shared/ai_client.py → GeminiFlashClient.score_all_professions_for_dimension()
    Signature: (dimension_name, user_reasoning_text, profession_contexts)

CATATAN POIN 15 — selection_type:
    GeminiFlashClient.score_all_professions_for_dimension() belum menerima
    parameter selection_type. Konteks selection_type saat ini dikelola langsung
    di IkigaiService._finalize_ikigai() yang memanggil gemini_client secara langsung.
    File ini mengekspos interface yang konsisten — selection_type diterima tapi
    TIDAK diteruskan ke gemini_client sampai ai_client.py diupdate.

FALLBACK r_raw = 0.5:
    Jika satu dimensi gagal, semua profesi di dimensi itu mendapat r_raw = 0.5
    (skor netral — tidak menguntungkan maupun merugikan profesi manapun).
    Dimensi yang gagal dicatat di failed_dimensions untuk audit.
"""

import asyncio
import logging
from typing import Dict, List, Tuple, Any, Optional

from app.shared.ai_client import gemini_client

logger = logging.getLogger(__name__)

DIMENSION_NAMES = [
    "what_you_love",
    "what_you_are_good_at",
    "what_the_world_needs",
    "what_you_can_be_paid_for",
]


class AIScoringService:
    """
    Wrapper untuk AI scoring relevansi teks jawaban user terhadap profesi kandidat.

    Untuk setiap dimensi, Gemini menilai seberapa relevan teks jawaban user
    terhadap setiap profesi kandidat.

    Output per profesi per dimensi: r_raw ∈ [0.0, 1.0]
    - 1.0 = sangat relevan
    - 0.0 = tidak relevan
    - 0.5 = fallback jika Gemini gagal (skor netral)
    """

    async def score_single_dimension(
        self,
        dimension_name: str,
        user_reasoning_text: str,
        profession_contexts: List[Dict[str, Any]],
        selection_type: str = "not_selected",  # diterima tapi belum diteruskan ke gemini_client
    ) -> List[Dict[str, Any]]:
        """
        Score satu dimensi: nilai relevansi teks user terhadap semua profesi kandidat.

        Memanggil Gemini 1x untuk dimensi ini.

        Args:
            dimension_name: Nama dimensi ('what_you_love', 'what_you_are_good_at',
                            'what_the_world_needs', 'what_you_can_be_paid_for')
            user_reasoning_text: Teks jawaban user untuk dimensi ini
            profession_contexts: List ringkasan profesi dari ProfessionDataService.
                                  get_profession_contexts_for_scoring()
            selection_type: "selected" atau "not_selected" — konteks tambahan.
                            Belum diteruskan ke gemini_client karena
                            GeminiFlashClient.score_all_professions_for_dimension()
                            belum menerima parameter ini. Akan diaktifkan setelah
                            ai_client.py diupdate untuk poin 15.

        Returns:
            List[{"profession_id": int, "r_raw": float}]
            r_raw di-clamp ke [0.0, 1.0], 4 desimal.

        Raises:
            Exception: Jika Gemini gagal — ditangani oleh score_all_dimensions() dengan fallback
        """
        raw_results = await gemini_client.score_all_professions_for_dimension(
            dimension_name=dimension_name,
            user_reasoning_text=user_reasoning_text,   # nama parameter yang benar di ai_client.py
            profession_contexts=profession_contexts,
            # selection_type tidak diteruskan — belum ada di signature ai_client.py
        )

        # Validasi dan clamp r_raw ke [0.0, 1.0]
        validated = []
        for item in raw_results:
            r = max(0.0, min(1.0, float(item["r_raw"])))
            validated.append({
                "profession_id": item["profession_id"],
                "r_raw": round(r, 4),
            })

        return validated

    async def score_all_dimensions(
        self,
        responses_text: Dict[str, str],
        profession_contexts: List[Dict[str, Any]],
        selection_types: Optional[Dict[str, str]] = None,
    ) -> Tuple[Dict[str, List[Dict]], List[str]]:
        """
        Jalankan scoring untuk semua 4 dimensi secara paralel via asyncio.gather().

        Setiap dimensi diproses independen. Jika satu dimensi gagal, dimensi lain
        tidak terpengaruh — profesi di dimensi yang gagal mendapat fallback r_raw = 0.5.

        Args:
            responses_text: Dict {dimension_name: user_reasoning_text} untuk 4 dimensi.
                            Dimensi yang NULL (belum dijawab) tidak dikirim ke Gemini.
            profession_contexts: List ringkasan semua profesi kandidat
            selection_types: Dict {dimension_name: "selected"|"not_selected"} (opsional).
                             Jika tidak diberikan, semua dianggap "not_selected".

        Returns:
            Tuple:
            - scores_per_dimension: Dict {dimension_name: List[{"profession_id", "r_raw"}]}
            - failed_dimensions: List nama dimensi yang gagal dan menggunakan fallback

        Contoh output:
            (
                {
                    "what_you_love":         [{"profession_id": 1, "r_raw": 0.87}, ...],
                    "what_you_are_good_at":  [{"profession_id": 1, "r_raw": 0.72}, ...],
                    "what_the_world_needs":  [{"profession_id": 1, "r_raw": 0.65}, ...],
                    "what_you_can_be_paid_for": [{"profession_id": 1, "r_raw": 0.91}, ...],
                },
                []  # tidak ada dimensi yang gagal
            )
        """
        if selection_types is None:
            selection_types = {}

        dim_names = list(responses_text.keys())

        # Buat coroutine untuk setiap dimensi yang ada teks jawabannya
        tasks = [
            self.score_single_dimension(
                dimension_name=dim,
                user_reasoning_text=responses_text[dim],
                profession_contexts=profession_contexts,
                selection_type=selection_types.get(dim, "not_selected"),
            )
            for dim in dim_names
        ]

        # Jalankan paralel — satu dimensi gagal tidak membatalkan yang lain
        results = await asyncio.gather(*tasks, return_exceptions=True)

        final: Dict[str, List[Dict]]  = {}
        failed_dimensions: List[str] = []

        for dim_name, result in zip(dim_names, results):
            if isinstance(result, Exception):
                # Fallback: semua profesi dapat r_raw = 0.5 (skor netral)
                logger.warning(
                    "ai_scoring_service: dimension failed, using neutral fallback",
                    dimension=dim_name,
                    error=str(result),
                    fallback_r_raw=0.5,
                    profession_count=len(profession_contexts),
                )
                final[dim_name] = [
                    {"profession_id": p["profession_id"], "r_raw": 0.5}
                    for p in profession_contexts
                ]
                failed_dimensions.append(dim_name)
            else:
                final[dim_name] = result

        if failed_dimensions:
            logger.warning(
                "ai_scoring_service: some dimensions used fallback",
                failed_dimensions=failed_dimensions,
                total_dimensions=len(dim_names),
            )

        return final, failed_dimensions


# Singleton instance — gunakan ini di IkigaiService
ai_scoring_service = AIScoringService()
