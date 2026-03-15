# app/api/v1/kenali_diri/career_profile/services/ai_service.py
import structlog
import json
from typing import List, Dict, Any
from app.shared.ai.base import BaseAIService

logger = structlog.get_logger()

# Mapping huruf RIASEC → nama tipe (pindah ke sini agar tersentralisasi)
RIASEC_LETTER_NAMES: Dict[str, str] = {
    "R": "Realistic",
    "I": "Investigative",
    "A": "Artistic",
    "S": "Social",
    "E": "Enterprising",
    "C": "Conventional",
}

class CareerProfileAIService(BaseAIService):
    """
    Service khusus untuk menangani semua logika AI di domain Career Profile.
    Menggunakan namespace 'kenali_diri/career_profile'.
    """
    
    def __init__(self):
        super().__init__(namespace="kenali_diri/career_profile")

    async def generate_ikigai_content(
        self, 
        profession_contexts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate konten Ikigai untuk daftar profesi."""
        
        def format_salary(path_info):
            if not path_info or not isinstance(path_info, dict):
                return '-'
            min_sal = path_info.get('salary_min', 0)
            max_sal = path_info.get('salary_max', 0)
            if min_sal == 0 and max_sal == 0:
                return '-'
            return f"Rp {min_sal//1000000} - {max_sal//1000000} juta/bulan"

        professions_block = ""
        for i, prof in enumerate(profession_contexts):
            professions_block += f"""
---
PROFESI {i+1}: {prof.get('name')} (ID: {prof.get('profession_id')})
Kode RIASEC: {prof.get('riasec_code')} ({prof.get('riasec_title')})
Deskripsi: {prof.get('about_description') or 'Tidak tersedia'}
Kecocokan Kepribadian: {prof.get('riasec_description') or 'Tidak tersedia'}
Aktivitas: {', '.join(prof.get('activities', [])[:5]) if prof.get('activities') else 'Tidak tersedia'}
Hard Skill: {', '.join(prof.get('hard_skills_required', [])[:5]) if prof.get('hard_skills_required') else 'Tidak tersedia'}
Soft Skill: {', '.join(prof.get('soft_skills_required', [])[:3]) if prof.get('soft_skills_required') else 'Tidak tersedia'}
Tools: {', '.join(prof.get('tools_required', [])[:4]) if prof.get('tools_required') else 'Tidak tersedia'}
Pasar Kerja: {', '.join(prof.get('market_insights', [])[:2]) if prof.get('market_insights') else 'Tidak tersedia'}
Gaji Entry: {format_salary(prof.get('entry_level_path'))}
Potensi Senior: {prof.get('senior_level_path', {}).get('title', '-')} — {format_salary(prof.get('senior_level_path'))}
"""
            
        prompt_vars = {
            "num_professions": len(profession_contexts),
            "professions_block": professions_block
        }
        
        try:
            parsed = await self.call_ai_json(
                prompt_key="ikigai_content_generation",
                prompt_vars=prompt_vars,
                max_tokens=6000,
                temperature=0.4,
                dimension="ikigai_content_generation"
            )
            
            if not isinstance(parsed, list):
                logger.error("ikigai_content_not_list")
                return []

            prof_name_map = {p["profession_id"]: p.get("name", "Profesi ini") for p in profession_contexts}
            validated = []
            for item in parsed:
                pid = item.get("profession_id")
                if not item.get("what_you_love"): item["what_you_love"] = "Deskripsi tidak tersedia."
                if not item.get("what_you_are_good_at"): item["what_you_are_good_at"] = "Deskripsi tidak tersedia."
                if not item.get("what_the_world_needs"): item["what_the_world_needs"] = "Deskripsi tidak tersedia."
                if not item.get("what_you_can_be_paid_for"): item["what_you_can_be_paid_for"] = "Deskripsi tidak tersedia."
                
                pname = prof_name_map.get(pid, "Profesi ini")
                if not item.get("what_you_love_option"): item["what_you_love_option"] = f"Menjalankan aktivitas harian sebagai {pname}."
                if not item.get("what_you_are_good_at_option"): item["what_you_are_good_at_option"] = f"Menguasai kompetensi teknis utama di bidang {pname}."
                if not item.get("what_the_world_needs_option"): item["what_the_world_needs_option"] = f"Memberikan dampak melalui peran {pname}."
                if not item.get("what_you_can_be_paid_for_option"): item["what_you_can_be_paid_for_option"] = f"Bekerja profesional dengan jenjang karier {pname}."
                
                validated.append(item)
                
            return validated
        except Exception as e:
            logger.error("ikigai_content_generation_failed", error=str(e))
            return []

    async def score_ikigai_batch(
        self,
        dimension_name: str,
        user_reasoning_text: str,
        profession_contexts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Scoring batch untuk satu dimensi Ikigai."""
        
        professions_block = ""
        for prof in profession_contexts:
            activities_str = ", ".join((prof.get("activities") or [])[:3]) or "Tidak tersedia"
            skills_str = ", ".join((prof.get("hard_skills_required") or [])[:3]) or "Tidak tersedia"
            about = (prof.get("about_description") or "")[:200]

            professions_block += (
                f"\n- Profesi ID {prof['profession_id']}: {prof['name']}\n"
                f"  Deskripsi singkat: {about}\n"
                f"  Aktivitas utama: {activities_str}\n"
                f"  Skill utama: {skills_str}"
            )
            
        from app.shared.ai_client import GeminiFlashClient
        dim_info = GeminiFlashClient.DIMENSION_LABELS.get(dimension_name, {
            "label": dimension_name,
            "description": "Nilai relevansi teks user terhadap profesi."
        })

        prompt_vars = {
            "dimension_label": dim_info["label"],
            "dimension_description": dim_info["description"],
            "user_reasoning_text": user_reasoning_text,
            "professions_block": professions_block.strip()
        }
        
        try:
            parsed = await self.call_ai_json(
                prompt_key="ikigai_scoring_batch",
                prompt_vars=prompt_vars,
                max_tokens=2000,
                temperature=0.1,
                dimension=f"ikigai_scoring_{dimension_name}"
            )
            
            if not isinstance(parsed, list):
                logger.error("ikigai_scoring_not_list", dimension=dimension_name)
                return []
                
            valid_ids = {p["profession_id"] for p in profession_contexts}
            result = []
            seen_ids = set()
            for item in parsed:
                pid = item.get("profession_id")
                if pid in valid_ids and pid not in seen_ids:
                    result.append({"profession_id": pid, "r_raw": round(float(item.get("r_raw", 0.5)), 4)})
                    seen_ids.add(pid)
            
            for pid in valid_ids:
                if pid not in seen_ids:
                    result.append({"profession_id": pid, "r_raw": 0.5})
            
            return result
        except Exception as e:
            logger.error("ikigai_scoring_failed", dimension=dimension_name, error=str(e))
            return [{"profession_id": p["profession_id"], "r_raw": 0.5} for p in profession_contexts]

    async def generate_recommendation_narrative(
        self,
        user_riasec_code: str,
        ikigai_responses: Dict[str, str],
        top_2_professions: List[Dict[str, Any]],
        profession_details: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate narasi rekomendasi final."""
        
        professions_block = ""
        profession_1_id = str(top_2_professions[0]["profession_id"]) if top_2_professions else "N/A"
        profession_2_id = (
            str(top_2_professions[1]["profession_id"]) if len(top_2_professions) > 1 else "N/A"
        )

        for prof in top_2_professions:
            pid = prof["profession_id"]
            match_pct = prof.get("total_score", 0)

            detail = next((p for p in profession_details if p["profession_id"] == pid), {})
            about      = detail.get("about_description", "-")
            activities = ", ".join(detail.get("activities", []))
            skills     = ", ".join(detail.get("hard_skills_required", []))

            professions_block += f"""
Profesi ID {pid}: {detail.get("name", "Unknown")} (Kecocokan: {match_pct:.1f}%)
Kode RIASEC: {detail.get("riasec_code", "-")}
Deskripsi singkat: {about}
Aktivitas utama: {activities}
Skill utama: {skills}
"""

        prompt_vars = {
            "user_riasec_code": user_riasec_code,
            "love_text": ikigai_responses.get("what_you_love", ""),
            "good_at_text": ikigai_responses.get("what_you_are_good_at", ""),
            "world_needs_text": ikigai_responses.get("what_the_world_needs", ""),
            "paid_for_text": ikigai_responses.get("what_you_can_be_paid_for", ""),
            "professions_block": professions_block.strip(),
            "profession_1_id": profession_1_id,
            "profession_2_id": profession_2_id
        }
        
        return await self.call_ai_json(
            prompt_key="recommendation_narrative",
            prompt_vars=prompt_vars,
            max_tokens=1500,
            temperature=0.6,
            dimension="recommendation_narrative"
        )

    async def generate_personality_about(
        self,
        riasec_code: str,
        riasec_title: str,
        riasec_description: str
    ) -> str:
        """Generate narasi kepribadian RIASEC."""
        
        letters      = list(riasec_code)
        letter_names = [RIASEC_LETTER_NAMES.get(l, l) for l in letters]

        if len(letters) == 1:
            sentence_2_template = (
                f"Caramu bekerja sepenuhnya didominasi oleh orientasi {letter_names[0]}."
            )
        elif len(letters) == 2:
            sentence_2_template = (
                f"Caramu bekerja juga dipengaruhi oleh pola pikir {letter_names[1]}."
            )
        else:
            sentence_2_template = (
                f"Caramu bekerja juga dipengaruhi oleh pola pikir {letter_names[1]} "
                f"dan gaya {letter_names[2]}."
            )

        prompt_vars = {
            "riasec_code": riasec_code,
            "riasec_title": riasec_title,
            "riasec_description": riasec_description or riasec_title,
            "letters_block": "\n".join(
                [f"- {l}: {RIASEC_LETTER_NAMES.get(l, l)}" for l in letters]
            ),
            "first_letter_name": letter_names[0],
            "sentence_2_template": sentence_2_template,
        }
        
        return await self.call_ai(
            prompt_key="personality_about",
            prompt_vars=prompt_vars,
            max_tokens=200,
            temperature=0.5,
            dimension="personality_about"
        )

# Singleton instance
career_profile_ai_service = CareerProfileAIService()
