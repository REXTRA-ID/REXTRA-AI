# tests/unit/test_ikigai_scoring.py
"""
Unit tests for Ikigai scoring utilities.
Verifies the official formulas for text score (15%) and click score (10%).
"""
import pytest
from app.shared.scoring_utils import (
    calculate_text_score,
    calculate_click_score,
    normalize_min_max
)

def test_normalize_min_max_basic():
    # Normal range: (0.8 - 0.2) / (1.0 - 0.2) = 0.6 / 0.8 = 0.75
    assert normalize_min_max(0.8, 0.2, 1.0) == 0.75
    # (0.5 - 0.0) / (1.0 - 0.0) = 0.5
    assert normalize_min_max(0.5, 0.0, 1.0) == 0.5

def test_normalize_min_max_zero_division():
    # If r_max == r_min, it should return 0.5 (neutral)
    assert normalize_min_max(0.8, 0.8, 0.8) == 0.5
    assert normalize_min_max(1.0, 1.0, 1.0) == 0.5

def test_normalize_min_max_edge_cases():
    # Should clamp results within [0, 1] even with rounding
    assert normalize_min_max(1.1, 0.0, 1.0) == 1.0
    assert normalize_min_max(-0.1, 0.0, 1.0) == 0.0
    # Formula: 15% * r_normalized * 100
    assert calculate_text_score(1.0) == 15.0
    assert calculate_text_score(0.0) == 0.0
    assert calculate_text_score(0.5) == 7.5
    assert calculate_text_score(0.33) == 4.95

def test_calculate_text_score_edge_cases():
    # Input out of bounds should be clamped to [0, 1]
    assert calculate_text_score(1.5) == 15.0
    assert calculate_text_score(-0.5) == 0.0

def test_calculate_click_score_selected():
    # Formula: 10% * r_raw * 100
    assert calculate_click_score(1.0, True) == 10.0
    assert calculate_click_score(0.0, True) == 0.0
    assert calculate_click_score(0.5, True) == 5.0
    assert calculate_click_score(0.75, True) == 7.5

def test_calculate_click_score_not_selected():
    # Should always be 0.0 if not selected, regardless of r_raw
    assert calculate_click_score(1.0, False) == 0.0
    assert calculate_click_score(0.5, False) == 0.0
    assert calculate_click_score(0.0, False) == 0.0

def test_calculate_click_score_edge_cases():
    # Input out of bounds should be clamped to [0, 1]
    assert calculate_click_score(1.5, True) == 10.0
    assert calculate_click_score(-0.1, True) == 0.0

def test_combined_score_logic_simulation():
    """Simulate total dimension score calculation for one profession."""
    r_raw = 0.8
    r_normalized = 0.9
    is_selected = True
    
    text_score = calculate_text_score(r_normalized)  # 15% * 0.9 * 100 = 13.5
    click_score = calculate_click_score(r_raw, is_selected) # 10% * 0.8 * 100 = 8.0
    
    total_dim_score = text_score + click_score # 21.5
    assert total_dim_score == 21.5
