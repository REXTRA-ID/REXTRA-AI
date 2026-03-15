import httpx
import asyncio
import json
import re
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.metrics import ai_request_counter, ai_response_time, ai_cost_tracker
import structlog

logger = structlog.get_logger()

class GeminiFlashClient:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.model = settings.OPENROUTER_MODEL
        self.timeout = 60

    async def chat_completion(
            self,
            messages: list,
            max_tokens: int = 2000,
            temperature: float = 0.7,
            dimension: str = "general"
    ) -> str:
        """
        Generic LLM call

        Args:
            messages: List of {role: "user"/"system", content: "..."}
            max_tokens: Max response length
            temperature: Creativity level
            dimension: For metrics tracking

        Returns:
            Generated text
        """
        retry_count = 0
        max_retries = 3

        while retry_count <= max_retries:
            try:
                # Measure response time
                with ai_response_time.labels(dimension=dimension).time():
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            f"{self.base_url}/chat/completions",
                            headers={
                                "Authorization": f"Bearer {self.api_key}",
                                "Content-Type": "application/json",
                                "HTTP-Referer": "http://localhost:8000",  # OpenRouter sering minta ini
                                "X-Title": "My FastAPI App",  # Opsional tapi disarankan
                            },
                            json={
                                "model": self.model,
                                "messages": messages,
                                "max_tokens": max_tokens,
                                "temperature": temperature
                            },
                            timeout=self.timeout
                        )

                        response.raise_for_status()
                        data = response.json()

                        # Extract response
                        generated_text = data["choices"][0]["message"]["content"]

                        # Track metrics
                        ai_request_counter.labels(
                            dimension=dimension,
                            status="success"
                        ).inc()

                        logger.info(
                            "ai_request_success",
                            dimension=dimension,
                            retry_count=retry_count
                        )

                        return generated_text

            except httpx.TimeoutException:
                retry_count += 1
                logger.warning(
                    "ai_request_timeout",
                    dimension=dimension,
                    retry_count=retry_count
                )
                if retry_count <= max_retries:
                    await asyncio.sleep(2 * retry_count)  # Exponential backoff
                    continue

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limit
                    retry_count += 1
                    wait_time = 2 ** retry_count
                    logger.warning(
                        "ai_rate_limit_hit",
                        wait_seconds=wait_time
                    )
                    if retry_count <= max_retries:
                        await asyncio.sleep(wait_time)
                        continue

                # Other HTTP errors - don't retry
                logger.error("ai_request_http_error", status_code=e.response.status_code)
                break

        # All retries failed
        ai_request_counter.labels(dimension=dimension, status="failed").inc()
        raise Exception(f"AI request failed after {retry_count} retries")
    
    def _clean_json_response(self, raw_response: str) -> str:
        """
        Clean AI response by removing markdown formatting
        
        AI models often wrap JSON in markdown code blocks like:
        ```json
        {...}
        ```
        
        This method extracts the pure JSON from such responses.
        
        Args:
            raw_response: Raw string from AI including potential markdown
            
        Returns:
            Clean JSON string ready for parsing
        """
        # Pattern to match ```json ... ``` or ``` ... ```
        json_block_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        match = re.search(json_block_pattern, raw_response)
        
        if match:
            return match.group(1).strip()
        
        # If no markdown block found, return as-is (might already be clean JSON)
        return raw_response.strip()
    
    def _parse_ikigai_response(self, raw_response: str) -> Dict[str, Any]:
        """
        Parse and validate AI response for Ikigai evaluation
        
        Args:
            raw_response: Raw string from AI
            
        Returns:
            Parsed dictionary with scores and analysis
        """
        try:
            cleaned = self._clean_json_response(raw_response)
            parsed = json.loads(cleaned)
            
            # Validate required keys
            if "scores" not in parsed:
                raise ValueError("Missing 'scores' key in AI response")
            
            scores = parsed["scores"]
            required_score_keys = ["K", "S", "B", "final_dimension_score"]
            
            for key in required_score_keys:
                if key not in scores:
                    raise ValueError(f"Missing '{key}' in scores")
                # Ensure values are floats between 0.0 and 1.0
                if not isinstance(scores[key], (int, float)):
                    raise ValueError(f"Score '{key}' must be numeric")
                scores[key] = max(0.0, min(1.0, float(scores[key])))
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(
                "ikigai_json_parse_error",
                error=str(e),
                raw_response=raw_response[:500]
            )
            # Return fallback response with zero scores
            return {
                "analysis": {
                    "topic_relevance": "Parse error - could not analyze",
                    "sentiment_analysis": "N/A",
                    "evidence_level": "N/A"
                },
                "scores": {
                    "K": 0.0,
                    "S": 0.0,
                    "B": 0.0,
                    "final_dimension_score": 0.0
                },
                "error": str(e)
            }
        except ValueError as e:
            logger.error(
                "ikigai_validation_error",
                error=str(e)
            )
            return {
                "analysis": {
                    "topic_relevance": f"Validation error: {str(e)}",
                    "sentiment_analysis": "N/A",
                    "evidence_level": "N/A"
                },
                "scores": {
                    "K": 0.0,
                    "S": 0.0,
                    "B": 0.0,
                    "final_dimension_score": 0.0
                },
                "error": str(e)
            }

    async def generate_ikigai_content(
        self,
        profession_contexts: list[Dict[str, Any]]
    ) -> list[Dict[str, Any]]:
        """
        Generate Ikigai dimensions content for multiple professions in a single batch call.

        Menghasilkan 8 field per profesi:
        - 4 field narasi (what_you_love, what_you_are_good_at, what_the_world_needs,
          what_you_can_be_paid_for): info card 2 kalimat — ditampilkan sebagai deskripsi
          penjelasan setelah user memilih
        - 4 field opsi (what_you_love_option, what_you_are_good_at_option,
          what_the_world_needs_option, what_you_can_be_paid_for_option): teks pilihan
          checkbox 1 kalimat — yang ditampilkan sebagai opsi soal di tiap dimensi,
          TIDAK menyebut nama jabatan sesuai brief

        Format opsi per dimensi (sesuai Brief Ikigai):
        - Love option      : deskripsi AKTIVITAS KERJA spesifik (bukan nama jabatan)
        - GoodAt option    : deskripsi TUGAS INTI yang bisa dikerjakan (bukan nama jabatan)
        - WorldNeeds option: deskripsi DAMPAK SOSIAL spesifik profesi ke masyarakat
        - PaidFor option   : deskripsi POLA KERJA + PENGHASILAN (bukan nama jabatan)
        """
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

        system_prompt = f"""Kamu adalah sistem backend penghasil konten tes karier Ikigai.

Di bawah ini terdapat {len(profession_contexts)} profesi. Untuk setiap profesi,
hasilkan DELAPAN (8) field konten sesuai format di bawah.

[DAFTAR PROFESI]
{professions_block}

[PENJELASAN 8 FIELD — WAJIB DIBACA]

KELOMPOK 1 — NARASI INFO CARD (4 field):
Field ini ditampilkan sebagai penjelasan setelah user memilih opsi.
Format: 2 kalimat, 25–40 kata, gunakan "kamu".

  what_you_love         → Ceritakan apa yang menyenangkan dan membuat semangat dari
                          aktivitas kerja profesi ini. Fokus: ketertarikan intrinsik,
                          hal yang membuat "lupa waktu".
  what_you_are_good_at  → Ceritakan keahlian dan kompetensi inti apa yang dibutuhkan
                          dan bisa dikuasai dalam profesi ini. Fokus: skill teknis khas.
  what_the_world_needs  → Ceritakan dampak sosial dan kontribusi nyata profesi ini
                          bagi masyarakat. Fokus: siapa yang terbantu, masalah apa
                          yang diselesaikan.
  what_you_can_be_paid_for → Ceritakan realitas pasar kerja, pola penghasilan, dan
                          peluang karier profesi ini. Fokus: stabilitas, prospek, gaji.

KELOMPOK 2 — TEKS OPSI CHECKBOX (4 field):
Field ini menjadi pilihan soal di tiap dimensi — HARUS mengikuti aturan ketat:
  ✗ JANGAN menyebut nama jabatan atau nama profesi secara eksplisit
  ✗ JANGAN generik ("mengerjakan tantangan menarik", "dampak nyata bagi masyarakat")
  ✓ HARUS spesifik ke karakteristik unik profesi ini
  ✓ Satu kalimat aktif, MAKS 15 kata, menggunakan kata kerja konkret
  ✓ Setiap profesi HARUS punya teks opsi yang berbeda dari profesi lain

  what_you_love_option         → Deskripsi AKTIVITAS KERJA harian yang khas dan spesifik
                                 profesi ini. Contoh baik: "Merancang arsitektur sistem
                                 backend yang menangani jutaan request secara bersamaan."
                                 Contoh buruk: "Mengerjakan tantangan yang menarik setiap hari."

  what_you_are_good_at_option  → Deskripsi TUGAS INTI yang membutuhkan keahlian khas profesi
                                 ini. Contoh baik: "Menganalisis kerentanan keamanan sistem
                                 dan merancang strategi mitigasi serangan siber."
                                 Contoh buruk: "Menyelesaikan masalah menggunakan keahlian inti."

  what_the_world_needs_option  → Deskripsi DAMPAK SOSIAL SPESIFIK profesi ini ke kelompok
                                 penerima manfaat tertentu. Contoh baik: "Melindungi data
                                 pribadi jutaan pengguna dari ancaman kebocoran dan serangan."
                                 Contoh buruk: "Memberikan dampak nyata bagi masyarakat."

  what_you_can_be_paid_for_option → Deskripsi POLA KERJA + PENGHASILAN yang realistis dan
                                 khas profesi ini. Contoh baik: "Bekerja remote-first dengan
                                 kompensasi senior berbasis seniority dan on-call allowance."
                                 Contoh buruk: "Pekerjaan dengan penghasilan kompetitif."

[ATURAN OUTPUT]
- Kembalikan HANYA JSON array valid
- Setiap item memiliki TEPAT 8 field: profession_id, what_you_love, what_you_are_good_at,
  what_the_world_needs, what_you_can_be_paid_for, what_you_love_option,
  what_you_are_good_at_option, what_the_world_needs_option, what_you_can_be_paid_for_option
- Narasi (4 field pertama): 2 kalimat, 25–40 kata, Bahasa Indonesia, gunakan "kamu"
- Opsi (4 field _option): 1 kalimat, MAKS 15 kata, kata kerja konkret, TIDAK menyebut
  nama jabatan, BERBEDA antar profesi
- Tidak ada teks tambahan sebelum/sesudah JSON

[FORMAT OUTPUT]
[
  {{
    "profession_id": <int>,
    "what_you_love": "2 kalimat narasi info card...",
    "what_you_are_good_at": "2 kalimat narasi info card...",
    "what_the_world_needs": "2 kalimat narasi info card...",
    "what_you_can_be_paid_for": "2 kalimat narasi info card...",
    "what_you_love_option": "1 kalimat MAKS 15 kata, aktivitas kerja spesifik tanpa nama jabatan...",
    "what_you_are_good_at_option": "1 kalimat MAKS 15 kata, tugas inti spesifik tanpa nama jabatan...",
    "what_the_world_needs_option": "1 kalimat MAKS 15 kata, dampak sosial spesifik tanpa nama jabatan...",
    "what_you_can_be_paid_for_option": "1 kalimat MAKS 15 kata, pola kerja+penghasilan spesifik tanpa nama jabatan..."
  }},
  ...
]"""

        messages = [
            {"role": "user", "content": system_prompt}
        ]
        
        try:
            raw_response = await self.chat_completion(
                messages=messages,
                max_tokens=6000,  # Dinaikkan ke 6000 — 5 profesi × 8 field butuh ~1000 token/profesi
                temperature=0.4,  # Sedikit lebih tinggi agar opsi lebih bervariasi antar profesi
                dimension="ikigai_content_generation"
            )
            
            cleaned = self._clean_json_response(raw_response)
            parsed = json.loads(cleaned)
            
            # Ensure it's a list
            if not isinstance(parsed, list):
                logger.error("ikigai_content_json_parse_error", error="Response is not a JSON array")
                return []

            # Validasi: pastikan setiap item punya semua 8 field
            # Jika _option field tidak ada, isi fallback berbasis nama profesi
            # agar tidak crash di service layer
            REQUIRED_FIELDS = [
                "profession_id",
                "what_you_love", "what_you_are_good_at",
                "what_the_world_needs", "what_you_can_be_paid_for",
                "what_you_love_option", "what_you_are_good_at_option",
                "what_the_world_needs_option", "what_you_can_be_paid_for_option",
            ]
            # Build lookup nama profesi untuk fallback opsi
            prof_name_map = {p["profession_id"]: p.get("name", "Profesi ini") for p in profession_contexts}

            validated = []
            for item in parsed:
                pid = item.get("profession_id")
                pname = prof_name_map.get(pid, "Profesi ini")
                acts = prof_name_map.get(pid, "")  # fallback minimal

                # Isi fallback _option jika kosong/tidak ada
                # PENTING: JANGAN sebut nama profesi (bisa bias jawaban user)
                # Gunakan aktivitas/skill dari profession_contexts sebagai fallback
                pc = next((p for p in profession_contexts if p.get("profession_id") == pid), {})
                activities = pc.get("activities", [])
                hard_skills = pc.get("hard_skills_required", [])

                act1 = activities[0] if activities else "merancang dan mengembangkan sistem"
                act2 = activities[1] if len(activities) > 1 else "mengoptimalkan performa sistem"
                skill1 = hard_skills[0] if hard_skills else "kemampuan teknis"
                skill2 = hard_skills[1] if len(hard_skills) > 1 else "analisis sistem"

                if not item.get("what_you_love_option"):
                    # Ambil aktivitas pertama dari data profesi, potong di kata ke-15
                    words = act1.split()
                    fallback = " ".join(words[:14]) + "." if len(words) > 14 else act1 + "."
                    item["what_you_love_option"] = fallback.capitalize()
                    logger.warning("ikigai_content_option_fallback",
                                   field="what_you_love_option", profession_id=pid)

                if not item.get("what_you_are_good_at_option"):
                    item["what_you_are_good_at_option"] = (
                        f"Menguasai dan menerapkan {skill1} serta {skill2} dalam pekerjaan sehari-hari."
                    )
                    logger.warning("ikigai_content_option_fallback",
                                   field="what_you_are_good_at_option", profession_id=pid)

                if not item.get("what_the_world_needs_option"):
                    words = act2.split()
                    fallback = " ".join(words[:14]) + " untuk kebutuhan nyata." if words else "Berkontribusi menyelesaikan masalah nyata yang dihadapi banyak orang."
                    item["what_the_world_needs_option"] = fallback.capitalize()
                    logger.warning("ikigai_content_option_fallback",
                                   field="what_the_world_needs_option", profession_id=pid)

                if not item.get("what_you_can_be_paid_for_option"):
                    item["what_you_can_be_paid_for_option"] = (
                        f"Berkarir di bidang {skill1} dengan kompensasi kompetitif dan jalur karier yang jelas."
                    )
                    logger.warning("ikigai_content_option_fallback",
                                   field="what_you_can_be_paid_for_option", profession_id=pid)

                validated.append(item)

            logger.info(
                "ikigai_content_generation_complete",
                professions_count=len(validated),
                fields_per_profession=8,
            )
            return validated
            
        except json.JSONDecodeError as e:
            # JSON terpotong karena max_tokens — coba recovery partial
            # Ambil item-item yang sudah lengkap sebelum titik putus
            logger.warning(
                "ikigai_content_json_truncated",
                error=str(e),
                attempting_partial_recovery=True,
            )
            try:
                # Cari item terakhir yang complete: cari "}" terakhir sebelum error
                raw_partial = self._clean_json_response(raw_response)
                # Potong sampai "}" terakhir lalu tutup array
                last_brace = raw_partial.rfind("}")
                if last_brace > 0:
                    partial_json = raw_partial[:last_brace + 1] + "]"
                    parsed_partial = json.loads(partial_json)
                    if isinstance(parsed_partial, list) and len(parsed_partial) > 0:
                        logger.info(
                            "ikigai_content_partial_recovery_success",
                            recovered_count=len(parsed_partial),
                        )
                        # Jalankan validasi fallback untuk item yang berhasil di-recover
                        prof_name_map = {p["profession_id"]: p.get("name", "Profesi ini") for p in profession_contexts}
                        validated_partial = []
                        for item in parsed_partial:
                            pid = item.get("profession_id")
                            pname = prof_name_map.get(pid, "Profesi ini")
                            if not item.get("what_you_love_option"):
                                item["what_you_love_option"] = f"Mengerjakan tugas inti {pname} secara langsung setiap hari."
                            if not item.get("what_you_are_good_at_option"):
                                item["what_you_are_good_at_option"] = f"Menyelesaikan pekerjaan teknis utama yang menjadi kompetensi inti {pname}."
                            if not item.get("what_the_world_needs_option"):
                                item["what_the_world_needs_option"] = f"Berkontribusi pada kebutuhan nyata masyarakat melalui peran {pname}."
                            if not item.get("what_you_can_be_paid_for_option"):
                                item["what_you_can_be_paid_for_option"] = f"Berkarir profesional sebagai {pname} dengan kompensasi pasar yang kompetitif."
                            if not item.get("what_you_love"):
                                item["what_you_love"] = "Deskripsi tidak tersedia."
                            if not item.get("what_you_are_good_at"):
                                item["what_you_are_good_at"] = "Deskripsi tidak tersedia."
                            if not item.get("what_the_world_needs"):
                                item["what_the_world_needs"] = "Deskripsi tidak tersedia."
                            if not item.get("what_you_can_be_paid_for"):
                                item["what_you_can_be_paid_for"] = "Deskripsi tidak tersedia."
                            validated_partial.append(item)
                        return validated_partial
            except Exception as recovery_err:
                logger.error("ikigai_content_partial_recovery_failed", error=str(recovery_err))
            return []

        except Exception as e:
            logger.error(
                "ikigai_content_generation_failed",
                error=str(e)
            )
            return []

    
    # =========================================================================
    # SCORING BATCH (Brief Ikigai Part 2 §4.3) — FUNGSI UTAMA
    # 1 call per dimensi, menilai SEMUA kandidat profesi sekaligus
    # =========================================================================

    SCORING_PROMPT_TEMPLATE = """\
Kamu adalah sistem evaluasi relevansi karier. Tugasmu adalah menilai \
seberapa relevan teks alasan pengguna dengan setiap profesi kandidat.

DIMENSI YANG DINILAI: {dimension_label}
({dimension_description})

TEKS JAWABAN PENGGUNA:
"{user_reasoning_text}"

DAFTAR PROFESI KANDIDAT:
{professions_block}

RUBRIK PENILAIAN (untuk menghitung r_raw per profesi):
Nilai r_raw = 0.40×K + 0.30×S + 0.30×B

Komponen K (Kecocokan Topik & Kata Kunci, bobot 40%):
- 0.00 = tidak ada kesamaan topik sama sekali
- 0.25 = relevan tapi sangat umum
- 0.50 = ada kata kunci atau skill yang terkait
- 0.75 = menyebut aktivitas/skill inti dengan konteks
- 1.00 = menyebut beberapa skill inti dengan konteks spesifik

Komponen S (Sentimen & Intensitas Minat, bobot 30%):
- 0.00 = negatif/menolak profesi ini
- 0.25 = netral
- 0.50 = positif lemah
- 0.75 = positif jelas
- 1.00 = positif sangat kuat dan konsisten

Komponen B (Spesifisitas & Bukti, bobot 30%):
- 0.00 = sangat vague, tidak ada bukti
- 0.25 = umum tanpa contoh
- 0.50 = ada contoh singkat
- 0.75 = contoh jelas dengan detail konteks
- 1.00 = contoh kuat + detail + menunjukkan pola

ATURAN OUTPUT:
- Kembalikan HANYA JSON array valid, tidak ada teks tambahan
- Hitung r_raw untuk SETIAP profesi di daftar
- r_raw harus dalam range 0.00 - 1.00, 2 desimal
- Nilai r_raw harus BERBEDA antar profesi (hindari semua nilai sama)
- Urutkan array berdasarkan profession_id (ascending)

FORMAT OUTPUT:
[
  {{"profession_id": <int>, "r_raw": <float>}},
  ...
]"""

    DIMENSION_LABELS = {
        "what_you_love": {
            "label": "What You Love (Apa yang Kamu Sukai)",
            "description": "Nilai seberapa relevan teks dengan aktivitas atau aspek pekerjaan yang disukai user. Fokus pada ekspresi ketertarikan, kesenangan, atau motivasi intrinsik."
        },
        "what_you_are_good_at": {
            "label": "What You Are Good At (Apa yang Kamu Kuasai)",
            "description": "Nilai seberapa relevan teks dengan kompetensi, keahlian, atau kemampuan yang dimiliki user. Fokus pada kata-kata yang menunjukkan kemampuan, pengalaman, atau keyakinan."
        },
        "what_the_world_needs": {
            "label": "What The World Needs (Apa yang Dibutuhkan Dunia)",
            "description": "Nilai seberapa relevan teks dengan dampak sosial, nilai manfaat, atau masalah yang ingin diselesaikan user. Fokus pada orientasi kontribusi, misi, atau tujuan."
        },
        "what_you_can_be_paid_for": {
            "label": "What You Can Be Paid For (Apa yang Bisa Dibayar)",
            "description": "Nilai seberapa relevan teks dengan realitas pasar kerja, preferensi gaya kerja, atau ekspektasi kompensasi user. Fokus pada pragmatisme karier."
        }
    }

    async def score_all_professions_for_dimension(
        self,
        dimension_name: str,
        user_reasoning_text: str,
        profession_contexts: list  # [{profession_id, name, about_description, activities, hard_skills_required}]
    ) -> list:
        """
        Scoring batch: 1 Gemini call per dimensi, menilai SEMUA kandidat profesi sekaligus.

        Sesuai Brief Ikigai Part 2 §4.3. Setiap call mengirim 1 teks user dan
        meminta penilaian relevansi terhadap semua kandidat profesi.

        Args:
            dimension_name: Salah satu dari IKIGAI_DIMENSIONS
            user_reasoning_text: Teks jawaban user untuk dimensi ini
            profession_contexts: List profesi dengan info ringkas untuk scoring

        Returns:
            List [{"profession_id": int, "r_raw": float}] — r_raw antara 0.0-1.0
            Jika parsing gagal, fallback r_raw = 0.5 untuk semua profesi
        """
        dim_info = self.DIMENSION_LABELS.get(dimension_name, {
            "label": dimension_name,
            "description": "Nilai relevansi teks user terhadap profesi."
        })

        # Build professions block (ringkas untuk efisiensi token)
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

        prompt = self.SCORING_PROMPT_TEMPLATE.format(
            dimension_label=dim_info["label"],
            dimension_description=dim_info["description"],
            user_reasoning_text=user_reasoning_text,
            professions_block=professions_block.strip()
        )

        messages = [{"role": "user", "content": prompt}]

        # Fallback data jika API gagal
        fallback = [{"profession_id": p["profession_id"], "r_raw": 0.5} for p in profession_contexts]

        try:
            raw_response = await self.chat_completion(
                messages=messages,
                max_tokens=2000,
                temperature=0.1,  # Rendah untuk konsistensi scoring numerik
                dimension=f"ikigai_scoring_{dimension_name}"
            )

            cleaned = self._clean_json_response(raw_response)
            parsed = json.loads(cleaned)

            if not isinstance(parsed, list):
                logger.error("ikigai_scoring_not_list", dimension=dimension_name)
                return fallback

            # Validasi & sanitasi output
            result = []
            profession_ids_expected = {p["profession_id"] for p in profession_contexts}
            seen_ids = set()

            for item in parsed:
                pid = item.get("profession_id")
                r_raw = item.get("r_raw", 0.5)

                if not isinstance(pid, int) or pid not in profession_ids_expected:
                    continue
                if pid in seen_ids:
                    continue

                r_raw = max(0.0, min(1.0, float(r_raw)))
                result.append({"profession_id": pid, "r_raw": round(r_raw, 4)})
                seen_ids.add(pid)

            # Tambahkan profesi yang tidak ada di response dengan fallback
            for prof in profession_contexts:
                if prof["profession_id"] not in seen_ids:
                    result.append({"profession_id": prof["profession_id"], "r_raw": 0.5})
                    logger.warning(
                        "ikigai_scoring_profession_missing_in_response",
                        profession_id=prof["profession_id"],
                        dimension=dimension_name
                    )

            logger.info(
                "ikigai_scoring_batch_complete",
                dimension=dimension_name,
                professions_scored=len(result)
            )
            return result

        except json.JSONDecodeError as e:
            logger.error(
                "ikigai_scoring_json_parse_error",
                dimension=dimension_name,
                error=str(e)
            )
            return fallback
        except Exception as e:
            logger.error(
                "ikigai_scoring_failed",
                dimension=dimension_name,
                error=str(e)
            )
            return fallback

    # =========================================================================
    # FUNGSI LAMA — menilai 1 profesi per call (tidak dipakai untuk scoring baru)
    # =========================================================================

    async def evaluate_ikigai_response(
        self,
        user_essay: str,
        profession_name: str,
        profession_description: str,
        dimension: str = "ikigai"
    ) -> Dict[str, Any]:
        """
        Evaluate user's essay response for Ikigai profession matching
        
        Uses weighted scoring formula: Score = 0.4K + 0.3S + 0.3B
        
        Scoring Criteria:
        - K (Kecocokan Topik / Topic Relevance): 40% weight
          Measures relevance of keywords/activities to the profession
          
        - S (Sentimen & Intensitas / Sentiment): 30% weight
          Measures affective emotions (joy, enthusiasm, passion)
          
        - B (Spesifisitas & Bukti / Evidence): 30% weight
          Measures concreteness of reasons/real experiences
        
        Args:
            user_essay: User's written response about why they're interested
            profession_name: Name of the profession being evaluated
            profession_description: Description of the profession
            dimension: Ikigai dimension being evaluated (for metrics)
            
        Returns:
            Dict containing:
            {
                "analysis": {
                    "topic_relevance": str,
                    "sentiment_analysis": str,
                    "evidence_level": str
                },
                "scores": {
                    "K": float (0.0-1.0),
                    "S": float (0.0-1.0),
                    "B": float (0.0-1.0),
                    "final_dimension_score": float (0.0-1.0)
                }
            }
        """
        system_prompt = """Anda adalah AI Career Specialist di REXTRA yang ahli dalam analisis psikometrik dan pencocokan karir. Tugas Anda adalah mengevaluasi respons esai pengguna untuk menentukan kecocokan mereka dengan profesi tertentu.

KRITERIA PENILAIAN (Skala 0.0 - 1.0):

1. **K (Kecocokan Topik)** - Bobot 40%:
   - Mengukur relevansi kata kunci, aktivitas, dan konsep yang disebutkan
   - 0.0 = Tidak ada relevansi sama sekali
   - 0.5 = Cukup relevan tapi tidak spesifik
   - 1.0 = Sangat relevan dan langsung terkait profesi

2. **S (Sentimen & Intensitas)** - Bobot 30%:
   - Mengukur emosi afektif (senang, antusias, passionate)
   - 0.0 = Tidak ada indikasi minat/emosi positif
   - 0.5 = Minat biasa-biasa saja
   - 1.0 = Sangat antusias dan benar-benar passionate

3. **B (Spesifisitas & Bukti)** - Bobot 30%:
   - Mengukur kekonkritan alasan dan pengalaman nyata
   - 0.0 = Tidak ada bukti/pengalaman spesifik
   - 0.5 = Ada beberapa contoh tapi kurang detail
   - 1.0 = Bukti kuat dengan pengalaman konkrit

INSTRUKSI OUTPUT:
- Hitung final_dimension_score = (0.4 * K) + (0.3 * S) + (0.3 * B)
- WAJIB output dalam format JSON valid TANPA markdown code block
- Jangan tambahkan teks apapun di luar JSON"""

        user_prompt = f"""Evaluasi respons esai berikut:

PROFESI: {profession_name}
DESKRIPSI PROFESI: {profession_description}

ESAI PENGGUNA:
\"\"\"{user_essay}\"\"\"

Berikan evaluasi dalam format JSON berikut TANPA markdown:
{{
  "analysis": {{
    "topic_relevance": "Penjelasan singkat kecocokan topik",
    "sentiment_analysis": "Penjelasan singkat sentimen/emosi",
    "evidence_level": "Penjelasan singkat bukti/pengalaman"
  }},
  "scores": {{
    "K": 0.0,
    "S": 0.0,
    "B": 0.0,
    "final_dimension_score": 0.0
  }}
}}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            raw_response = await self.chat_completion(
                messages=messages,
                max_tokens=1000,
                temperature=0.3,  # Lower temperature for consistent scoring
                dimension=dimension
            )
            
            result = self._parse_ikigai_response(raw_response)
            
            logger.info(
                "ikigai_evaluation_complete",
                profession=profession_name,
                dimension=dimension,
                final_score=result["scores"]["final_dimension_score"]
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "ikigai_evaluation_failed",
                profession=profession_name,
                error=str(e)
            )
            # Return fallback with zero scores
            return {
                "analysis": {
                    "topic_relevance": f"Evaluation failed: {str(e)}",
                    "sentiment_analysis": "N/A",
                    "evidence_level": "N/A"
                },
                "scores": {
                    "K": 0.0,
                    "S": 0.0,
                    "B": 0.0,
                    "final_dimension_score": 0.0
                },
                "error": str(e)
            }


# Singleton instance
gemini_client = GeminiFlashClient()