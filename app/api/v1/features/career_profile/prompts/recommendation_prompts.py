# app/api/v1/categories/career_profile/prompts/recommendation_prompts.py
"""
Prompt templates untuk narasi rekomendasi final dan narasi kepribadian.
Dipindahkan dari services/recommendation_narrative_service.py dan
services/personality_service.py ke sini sesuai brief Part 3.
"""

# ===========================================================================
# RECOMMENDATION NARRATIVE PROMPT — Brief Part 3 §3
# Dipakai oleh: RecommendationNarrativeService
# ===========================================================================

RECOMMENDATION_NARRATIVE_PROMPT = """
Kamu adalah konselor karier berbasis data. Tugasmu adalah menulis narasi personal
berdasarkan jawaban pengguna dalam Tes Ikigai.

PROFIL RIASEC PENGGUNA: {user_riasec_code}

JAWABAN PENGGUNA PER DIMENSI IKIGAI:
---
Dimensi 1 — What You Love (Apa yang Kamu Sukai):
"{love_text}"

Dimensi 2 — What You Are Good At (Apa yang Kamu Kuasai):
"{good_at_text}"

Dimensi 3 — What The World Needs (Apa yang Dibutuhkan Dunia):
"{world_needs_text}"

Dimensi 4 — What You Can Be Paid For (Apa yang Bisa Dibayar):
"{paid_for_text}"
---

DUA PROFESI YANG DIREKOMENDASIKAN:
{professions_block}

TUGAS:
Hasilkan 6 teks narasi:
1. Ringkasan Dimensi 1 (ikigai_profile_summary.what_you_love)
2. Ringkasan Dimensi 2 (ikigai_profile_summary.what_you_are_good_at)
3. Ringkasan Dimensi 3 (ikigai_profile_summary.what_the_world_needs)
4. Ringkasan Dimensi 4 (ikigai_profile_summary.what_you_can_be_paid_for)
5. Alasan kecocokan Profesi ID {profession_1_id} (match_reasoning)
6. Alasan kecocokan Profesi ID {profession_2_id} (match_reasoning)

ATURAN PENULISAN:

UNTUK RINGKASAN DIMENSI (teks 1-4):
- 2-3 kalimat efektif per dimensi (60-90 kata)
- Bersifat GENERAL — tidak menyebut nama profesi apapun
- Tulis sebagai refleksi diri pengguna: gunakan "Kamu..."
- Abstraksi dari jawaban pengguna — bukan parafrase langsung
- Bahasa Indonesia yang natural dan empatik

UNTUK ALASAN KECOCOKAN PROFESI (teks 5-6):
- Tepat 2 kalimat (template wajib):
  Kalimat 1: "Profesi ini cocok karena [hubungan minat/kekuatan dengan aktivitas inti profesi]."
  Kalimat 2: "[Implikasi praktis — bagaimana pengalaman/pola kerja pengguna berkembang dalam profesi ini]."

ATURAN OUTPUT:
- WAJIB mengembalikan JSON valid.
- JANGAN sertakan markdown block atau backticks.
- Struktur JSON wajib sama persis dengan format di bawah.

FORMAT JSON OUTPUT:
{{
  "ikigai_profile_summary": {{
    "what_you_love": "...",
    "what_you_are_good_at": "...",
    "what_the_world_needs": "...",
    "what_you_can_be_paid_for": "..."
  }},
  "match_reasoning": {{
    "{profession_1_id}": "...",
    "{profession_2_id}": "..."
  }}
}}
"""


# ===========================================================================
# PERSONALITY ABOUT PROMPT — Brief Part 3 §4
# Dipakai oleh: PersonalityService
# ===========================================================================

PERSONALITY_ABOUT_PROMPT = """
Kamu adalah penulis konten karier. Tugasmu adalah memformat ulang deskripsi kode RIASEC
menjadi narasi personal yang hangat dan mudah dipahami remaja/mahasiswa.

KODE RIASEC: {riasec_code}
JUDUL KODE: {riasec_title}
DESKRIPSI ASLI DARI DATABASE:
"{riasec_description}"

NAMA TIPE HURUF:
{letters_block}

TUGAS:
Tulis tepat 3 kalimat narasi dengan template wajib:

Kalimat 1: "Kode {riasec_code} menunjukkan bahwa kekuatan utamamu adalah tipe {first_letter_name}."
Kalimat 2: "{sentence_2_template}"
Kalimat 3: "Sinergi ini membuatmu cenderung menjadi [rangkuman karakter dari deskripsi — 1 kalimat singkat, padat, positif]."

ATURAN:
- Kalimat 1 dan 2 WAJIB menggunakan template persis (sudah disediakan di atas, jangan ubah)
- Kalimat 3 bebas tapi harus diturunkan dari deskripsi asli
- Maksimum 30 kata untuk kalimat 3
- Bahasa Indonesia yang hangat dan memotivasi
- Gunakan kata "kamu" (bukan "Anda")

ATURAN OUTPUT:
- Kembalikan HANYA teks 3 kalimat, tidak ada label, tidak ada JSON
- Pisahkan tiap kalimat dengan newline
"""


# Mapping huruf RIASEC → nama tipe
RIASEC_LETTER_NAMES: dict[str, str] = {
    "R": "Realistic",
    "I": "Investigative",
    "A": "Artistic",
    "S": "Social",
    "E": "Enterprising",
    "C": "Conventional",
}
