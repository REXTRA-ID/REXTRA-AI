import pytest
from app.api.v1.categories.career_profile.utils.classification import classify_riasec_code

def test_single_code_classification():
    """Test single dominant type"""
    scores = {"R": 45, "I": 28, "A": 25, "S": 22, "E": 20, "C": 18}
    code, code_type = classify_riasec_code(scores)
    
    assert code == "R"
    assert code_type == "single"

def test_dual_code_classification():
    """Test dual types"""
    scores = {"R": 42, "I": 38, "A": 25, "S": 22, "E": 20, "C": 18}
    code, code_type = classify_riasec_code(scores)
    
    assert code == "RI"
    assert code_type == "dual"

def test_triple_code_classification():
    """Test triple types"""
    scores = {"R": 38, "I": 36, "A": 34, "S": 25, "E": 22, "C": 20}
    code, code_type = classify_riasec_code(scores)
    
    assert code == "RIA"
    assert code_type == "triple"

def test_all_scores_equal():
    """Test edge case: all scores equal"""
    scores = {"R": 30, "I": 30, "A": 30, "S": 30, "E": 30, "C": 30}
    code, code_type = classify_riasec_code(scores)
    
    # Should return triple (first 3 in dict order)
    assert len(code) == 3
    assert code_type == "triple"
