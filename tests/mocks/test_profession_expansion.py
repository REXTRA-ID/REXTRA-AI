import pytest
from unittest.mock import MagicMock
from app.api.v1.categories.career_profile.services.profession_expansion import ProfessionExpansionService

@pytest.fixture
def expansion_service():
    db_mock = MagicMock()
    service = ProfessionExpansionService(db_mock)
    
    service.riasec_repo = MagicMock()
    return service

def test_expansion_logic_tier_2_generation(expansion_service):
    """Test 4: Memastikan permutasi hanya dari Top 3 (RIA)"""
    user_code = "RIA"
    user_scores = {"R": 50, "I": 48, "A": 46, "S": 20, "E": 18, "C": 15}
    
    # Ambil top 3 (manual untuk verifikasi)
    # sorted -> R, I, A
    
    congruent_codes = expansion_service._generate_congruent_codes(user_code, ["R", "I", "A"])
    
    # Harus ada 5 kode (3! - 1 user_code)
    assert len(congruent_codes) == 5
    assert "RAI" in congruent_codes
    assert "IRA" in congruent_codes
    # Pastikan tidak ada kode di luar Top 3 (tidak boleh ada S, E, atau C)
    assert not any('S' in code for code in congruent_codes)
    assert not any('E' in code for code in congruent_codes)

def test_expansion_logic_subset_generation(expansion_service):
    """Test 4: Memastikan subset (2-letter) hanya dari Top 3"""
    top_3 = ["R", "I", "A"]
    subset_codes = expansion_service._generate_subset_codes(top_3)
    
    # Permutasi 2 dari 3 = 6 kode: RI, RA, IR, IA, AI, AR
    assert len(subset_codes) == 6
    assert "RI" in subset_codes
    assert "IA" in subset_codes
    assert "RE" not in subset_codes # E bukan top 3

def test_expansion_flat_scores_edge_case(expansion_service):
    """Test 4b: Skor mepet tetap harus ambil top 3 tertinggi secara ketat"""
    user_code = "RIA"
    # S, E, C mepet tapi tetap di bawah A
    user_scores = {"R": 40, "I": 39, "A": 38, "S": 37, "E": 36, "C": 35}
    
    # Jalankan expand_candidates (kita hanya cek summary-nya)
    # Kita mock method repo agar mengembalikan list kosong supaya dia lanjut ke semua tier
    expansion_service.riasec_repo.get_riasec_code_by_string.return_value = MagicMock(id=1)
    
    result = expansion_service.expand_candidates(user_code, 1, user_scores)
    
    # Verifikasi metadata
    assert result["user_top_3_types"] == ["R", "I", "A"]
    # Cek apakah congruent_codes_used hanya berisi kombinasi RIA
    used_codes = result["expansion_summary"].get("congruent_codes_used", [])
    assert "RAI" in used_codes
    assert "RIS" not in used_codes # S tidak boleh masuk meskipun skornya 37