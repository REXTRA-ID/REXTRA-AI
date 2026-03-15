# app/api/v1/categories/career_profile/services/personality_service.py
"""
PersonalityService — Generate narasi kepribadian RIASEC via Gemini.
"""
import structlog
from app.api.v1.features.career_profile.services.ai_service import career_profile_ai_service

logger = structlog.get_logger()

class PersonalityService:
    @staticmethod
    async def get_personality_about_text(
        riasec_code: str,
        riasec_title: str,
        riasec_description: str,
        redis_client,
    ) -> str:
        """
        Ambil narasi 'Tentang Kode' dari Redis atau generate via Gemini.
        Di-cache per kode RIASEC — tidak personal, sama untuk semua user.
        """
        cache_key = f"personality_about:{riasec_code}"

        # Cek Redis cache dulu
        if redis_client:
            try:
                cached = await redis_client.get(cache_key)
                if cached:
                    return cached.decode("utf-8")
            except Exception:
                pass  # Redis down — lanjut ke Gemini

        try:
            # Panggil CareerProfileAIService (Prompt & AI logic tersentralisasi)
            text = await career_profile_ai_service.generate_personality_about(
                riasec_code=riasec_code,
                riasec_title=riasec_title,
                riasec_description=riasec_description
            )

            # Simpan ke Redis TTL 7 hari
            if redis_client and text:
                try:
                    await redis_client.setex(cache_key, 7 * 24 * 3600, text)
                except Exception:
                    pass

            return text

        except Exception as e:
            logger.error("personality_about_generation_failed", riasec_code=riasec_code, error=str(e))
            return (
                "Kekuatan utamamu tergambar dari kode ini. "
                "Memiliki potensi besar jika dikembangkan dengan baik."
            )
