# app/api/v1/categories/career_profile/services/profession_data_service.py
"""
ProfessionDataService — Service layer untuk query dan persiapan konteks data profesi.

Sesuai spesifikasi:
    Brief Ikigai Part 1, Bagian 8: "Query multi-table data profesi (raw SQL)"
    Brief Ikigai Part 2, Bagian 10: "Tambah method get_profession_contexts_for_scoring()"

Service ini adalah facade di atas ProfessionRepository.
Tugas utama:
1. Sediakan data profesi diperkaya (join multi-tabel) untuk konten Ikigai
2. Sediakan versi ringkas untuk AI scoring
3. Sediakan data lengkap untuk narasi rekomendasi final

Semua query aktual ada di ProfessionRepository — file ini adalah titik entry
resmi yang digunakan oleh IkigaiService.

CATATAN PERBEDAAN DENGAN profession_expansion.py:
    profession_expansion.py    → logika BISNIS ekspansi kandidat RIASEC
                                  (hitung congruence score, tier 1/2/3, pool 5–30 profesi)
    profession_data_service.py → facade QUERY untuk detail konteks profesi
                                  (tidak ada logika bisnis, hanya delegasi ke repo)

KOREKSI DARI BUG REPORT:
    Dokumen asli mengusulkan parameter session_id + display_limit — SALAH.
    Signature repo aktual adalah profession_ids: List[int].
    File ini meneruskan profession_ids sesuai signature yang benar.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.api.v1.kenali_diri.career_profile.repositories.profession_repo import ProfessionRepository


class ProfessionDataService:
    """
    Service untuk menyiapkan konteks data profesi yang dibutuhkan oleh:
    - IkigaiService._generate_ikigai_content()  → konten dimensi + opsi checkbox Flutter
    - IkigaiService._finalize_ikigai()           → scoring AI + narasi rekomendasi
    """

    def __init__(self, db: Session):
        self.db   = db
        self.repo = ProfessionRepository(db)

    def get_profession_contexts_for_ikigai(
        self, profession_ids: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Query data profesi lengkap untuk generate konten dimensi Ikigai.

        Digunakan oleh: IkigaiService._generate_ikigai_content()
        Data yang dikumpulkan (join multi-tabel):
            - professions JOIN riasec_codes
            - profession_activities (sort_order ASC, max 5)
            - profession_skill_rel JOIN skills (hard + soft)
            - profession_tool_rel JOIN tools (wajib)

        Args:
            profession_ids: List ID profesi display kandidat (biasanya 5 profesi teratas,
                            yaitu kandidat dengan display_order <= 5)

        Returns:
            List dict konteks profesi, siap dikirim ke AIContentService / Gemini
        """
        return self.repo.get_profession_contexts_for_ikigai(profession_ids=profession_ids)

    def get_profession_contexts_for_scoring(
        self, profession_ids: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Query ringkasan data profesi untuk AI scoring.

        Digunakan oleh: IkigaiService._finalize_ikigai() → AIScoringService
        Mencakup SEMUA kandidat (opsi + pool), bukan hanya top-5 display.

        Perbedaan dengan get_profession_contexts_for_ikigai():
        - Mencakup lebih banyak profesi (5–30 dari pool ekspansi)
        - Data lebih ringkas: nama + aktivitas (5) + hard skill (3)
        - Tidak include market_insights & career_paths (tidak relevan untuk scoring)

        Args:
            profession_ids: List ID semua kandidat profesi dalam sesi
                            (ambil dari ikigai_candidate_professions)

        Returns:
            List dict ringkasan profesi untuk prompt AI scoring
        """
        return self.repo.get_profession_contexts_for_scoring(profession_ids=profession_ids)

    def get_profession_contexts_for_recommendation(
        self, profession_ids: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Query data profesi lengkap untuk generate narasi rekomendasi final.

        Digunakan oleh: IkigaiService._finalize_ikigai() setelah top 2 profesi ditentukan.
        Hanya mengambil 2 profesi terpilih — bukan seluruh pool.

        Args:
            profession_ids: List 2 ID profesi teratas (top_profession_1 & top_profession_2)

        Returns:
            List dict konteks profesi lengkap untuk RecommendationNarrativeService
        """
        return self.repo.get_profession_contexts_for_recommendation(
            profession_ids=profession_ids
        )

    def get_by_ids(self, profession_ids: List[int]) -> List[Any]:
        """
        Ambil objek Profession berdasarkan daftar ID.

        Digunakan oleh: ResultService untuk enrich nama profesi di response API.

        Args:
            profession_ids: List integer ID profesi

        Returns:
            List objek Profession SQLAlchemy
        """
        return self.repo.get_by_ids(profession_ids=profession_ids)
