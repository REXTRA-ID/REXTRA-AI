# app/shared/scoring_utils.py
"""
Scoring Utilities for Kenali Diri Application

This module contains helper functions for calculating and normalizing scores
in the career profiling system, particularly for Ikigai evaluation.

Formula Resmi (Brief Ikigai Part 2 §3.2):
  T_p,d = 15% × R_normalized(p,d) × 100    → range 0.0–15.0
  A_p,d = 10% × C_p,d × R_raw(p,d) × 100  → range 0.0–10.0 (hanya jika dipilih)
  S_p,d = T_p,d + A_p,d                    → range 0.0–25.0
  Score_total(p) = S_p,love + S_p,good_at + S_p,world + S_p,paid  → range 0–100
"""

from typing import Optional

# =============================================================================
# FUNGSI RESMI (Brief Ikigai Part 2 §3.2)
# =============================================================================

def calculate_text_score(r_normalized: float) -> float:
    """
    Hitung text score per profesi per dimensi.

    Formula: T_p,d = 15% × R_normalized(p,d) × 100
    Range output: 0.0 – 15.0

    Args:
        r_normalized: Nilai normalisasi min-max dari r_raw Gemini (0.0–1.0)

    Returns:
        Float antara 0.0 dan 15.0
    """
    r_normalized = max(0.0, min(1.0, r_normalized))
    return round(0.15 * r_normalized * 100, 4)


def calculate_click_score(r_raw: float, is_selected: bool) -> float:
    """
    Hitung click score per profesi per dimensi (confidence-based).

    Formula: A_p,d = 10% × C_p,d × R_raw(p,d) × 100
      - Menggunakan R_raw (bukan R_normalized) sebagai ukuran keyakinan AI
        sebelum distorsi normalisasi (confidence-based adjustment)
      - C_p,d = 1 jika profesi ini yang dipilih user di dimensi ini, 0 jika tidak
    Range output: 0.0 – 10.0

    Args:
        r_raw: Nilai mentah dari Gemini sebelum normalisasi (0.0–1.0)
        is_selected: True jika profesi ini yang dipilih user di dimensi ini

    Returns:
        Float antara 0.0 dan 10.0
    """
    if not is_selected:
        return 0.0
    r_raw = max(0.0, min(1.0, r_raw))
    return round(0.10 * r_raw * 100, 4)


def normalize_min_max(r_raw: float, r_min: float, r_max: float) -> float:
    """
    Normalisasi nilai r_raw ke rentang [0.0, 1.0] berdasarkan min-max satu dimensi.

    PENTING: Jika r_max == r_min (semua profesi punya skor identik),
    maka r_norm diset ke 0.5 (skor netral) agar tidak ada profesi yang
    diuntungkan atau dirugikan secara tidak adil.

    Args:
        r_raw: Skor mentah dari Gemini
        r_min: Skor terendah dalam satu dimensi
        r_max: Skor tertinggi dalam satu dimensi

    Returns:
        Float r_norm dalam rentang [0.0, 1.0]
    """
    denom = r_max - r_min
    if denom <= 0:
        return 0.5
    
    r_norm = (r_raw - r_min) / denom
    return max(0.0, min(1.0, round(r_norm, 4)))


# =============================================================================
# FUNGSI LAMA — DEPRECATED (Dihapus)
# =============================================================================
