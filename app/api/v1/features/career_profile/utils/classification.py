# app/api/v1/categories/career_profile/utils/classification.py
"""
CATATAN PENTING — JANGAN GUNAKAN FUNGSI classify_riasec_code() DI FILE INI
UNTUK LOGIKA BARU.

File ini dipertahankan untuk backward compatibility import path. Isi logika
lama (yang salah) sudah diganti dengan delegation ke riasec_service.py yang
merupakan sumber kebenaran tunggal untuk klasifikasi RIASEC.

Logika klasifikasi yang lengkap dan benar ada di:
    app/api/v1/categories/career_profile/services/riasec_service.py
    → fungsi: classify_riasec_code()  — return (code, type, is_inconsistent)
    → fungsi: sort_scores()
    → fungsi: validate_scores()

Perbedaan return type antara versi lama dan baru:
    LAMA: classify_riasec_code(scores) → Tuple[str, str]
    BARU: classify_riasec_code(scores) → Tuple[str, str, bool]  ← tambah is_inconsistent

Lihat Brief RIASEC v2.0 "Temuan dari Bedah Project" untuk konteks perbaikan ini.
"""

# Re-export dari riasec_service agar import lama tidak rusak.
# Kode yang import dari utils/classification akan otomatis mendapat
# implementasi yang benar tanpa perlu mengubah import mereka.
from app.api.v1.features.career_profile.services.riasec_service import (
    classify_riasec_code,
    sort_scores,
    validate_scores,
)

__all__ = [
    "classify_riasec_code",
    "sort_scores",
    "validate_scores",
]
