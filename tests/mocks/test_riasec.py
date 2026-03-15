import pytest
from typing import Dict
from app.api.v1.categories.career_profile.services.riasec_service import classify_riasec_code

def test_single_code_classification():
    # Test 1: Single Code
    scores = {"R": 50, "I": 30, "A": 25, "S": 20, "E": 15, "C": 10}
    code, c_type, is_inconsistent = classify_riasec_code(scores)
    
    assert code == "R"
    assert c_type == "single"
    assert is_inconsistent is False

def test_dual_code_classification():
    # Test 2: Dual Code
    scores = {"R": 45, "I": 42, "A": 30, "S": 25, "E": 20, "C": 15}
    code, c_type, is_inconsistent = classify_riasec_code(scores)
    
    assert code == "RI"
    assert c_type == "dual"
    assert is_inconsistent is False

def test_triple_code_classification():
    # Test 3: Triple Code
    scores = {"R": 38, "I": 36, "A": 34, "S": 30, "E": 28, "C": 25}
    code, c_type, is_inconsistent = classify_riasec_code(scores)
    
    assert code == "RIA"
    assert c_type == "triple"
    assert is_inconsistent is False

def test_inconsistent_profile():
    # Inconsistent (R and S are opposite)
    scores = {"R": 50, "S": 45, "A": 10, "I": 5, "E": 5, "C": 5}
    code, c_type, is_inconsistent = classify_riasec_code(scores)
    
    assert "R" in code and "S" in code
    assert is_inconsistent is True

if __name__ == "__main__":
    # List of test cases
    test_cases = [
        {"name": "Test 1 (Single)", "scores": {"R": 50, "I": 30, "A": 25, "S": 20, "E": 15, "C": 10}, "exp_code": "R"},
        {"name": "Test 2 (Dual)", "scores": {"R": 45, "I": 42, "A": 30, "S": 25, "E": 20, "C": 15}, "exp_code": "RI"},
        {"name": "Test 3 (Triple)", "scores": {"R": 38, "I": 36, "A": 34, "S": 30, "E": 28, "C": 25}, "exp_code": "RIA"},
    ]

    for tc in test_cases:
        code, c_type, inc = classify_riasec_code(tc["scores"])
        status = "✅ PASSED" if code == tc["exp_code"] else "❌ FAILED"
        print(f"{tc['name']}: Result={code}, Type={c_type} | {status}")