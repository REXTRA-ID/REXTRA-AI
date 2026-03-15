#!/usr/bin/env python3
"""
End-to-End (E2E) Real Test Script

This script performs a complete real test of the Kenali Diri Career Profiling API,
including RIASEC assessment and AI-powered Ikigai evaluation.

Usage:
    python scripts/e2e_real_test.py

Requirements:
    - API server running at http://localhost:8000
    - Database seeded with RIASEC codes and digital professions
    - Valid OpenRouter API key configured
"""
import json
import time
import random
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print("❌ ERROR: 'requests' library not installed.")
    print("   Install with: pip install requests")
    sys.exit(1)


# =============================================================================
# CONFIGURATION
# =============================================================================
BASE_URL = "http://localhost:8010/api/v1"
USER_ID = "ef9cf8e8-46b1-4e91-89d0-40f6c824319e"  # UUID format

HEADERS = {
    "x-user-id": USER_ID,
    "Content-Type": "application/json"
}

# RIASEC question mapping
RIASEC_QUESTIONS = {
    "R": list(range(1, 13)),      # Realistic
    "I": list(range(13, 25)),     # Investigative
    "A": list(range(25, 37)),     # Artistic
    "S": list(range(37, 49)),     # Social
    "E": list(range(49, 61)),     # Enterprising
    "C": list(range(61, 73)),     # Conventional
}

IKIGAI_ESSAYS = {
    "what_you_love": (
        "Saya sangat menyukai coding dan memecahkan masalah logika yang kompleks. "
        "Ada kebahagiaan tersendiri saat berhasil debugging dan menemukan solusi elegan. "
        "Saya selalu excited ketika belajar teknologi baru dan menerapkannya di project nyata. "
        "Bekerja dengan data dan membangun sistem backend yang scalable adalah hal yang membuat saya semangat."
    ),
    "what_you_are_good_at": (
        "Saya menguasai Python dan SQL optimization dengan baik berdasarkan pengalaman 3 tahun. "
        "Saya pernah membangun RESTful API yang melayani 10,000+ request per menit. "
        "Kemampuan problem-solving dan analytical thinking saya sudah teruji di berbagai hackathon. "
        "Saya juga familiar dengan Docker, Kubernetes, dan cloud infrastructure dasar."
    ),
    "what_the_world_needs": (
        "Dunia butuh sistem yang efisien, aman, dan dapat diandalkan untuk menunjang transformasi digital. "
        "Industri membutuhkan engineer yang bisa membangun infrastruktur backend yang scalable. "
        "Banyak perusahaan yang struggle dengan legacy system dan butuh modernisasi. "
        "Dengan skill ini saya bisa membantu organisasi menjadi lebih efisien dan data-driven."
    ),
    "what_you_can_be_paid_for": (
        "Software Engineering adalah skill high demand di industri teknologi saat ini. "
        "Gaji untuk Backend Developer sangat kompetitif dengan range 15-50 juta per bulan di Indonesia. "
        "Remote work opportunities sangat banyak untuk role ini. "
        "Career progression jelas dari Junior ke Senior ke Staff/Principal Engineer."
    ),
}

DIMENSION_KEYS = ["what_you_love", "what_you_are_good_at", "what_the_world_needs", "what_you_can_be_paid_for"]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def print_header():
    print("\n" + "=" * 70)
    print("🚀 KENALI DIRI - End-to-End Real Test")
    print("=" * 70)
    print(f"   Base URL: {BASE_URL}")
    print(f"   Started:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

def print_step(step: int, total: int, message: str):
    print(f"\n[{step}/{total}] {message}")
    print("-" * 50)

def print_success(message: str):
    print(f"✅ {message}")

def print_error(message: str, response=None):
    print(f"❌ {message}")
    if response is not None:
        print(f"   Status Code: {response.status_code}")
        try:
            print(f"   Response: {json.dumps(response.json(), indent=2)[:500]}")
        except:
            print(f"   Response: {response.text[:500]}")

def print_info(message: str):
    print(f"ℹ️  {message}")

def generate_riasec_answers(dominant_types: list = ["I", "R"]) -> list:
    answers = []
    for question_id in range(1, 73):
        question_type = None
        for type_code, questions in RIASEC_QUESTIONS.items():
            if question_id in questions:
                question_type = type_code
                break
        
        if question_type in dominant_types:
            score = random.choice([4, 5, 5, 5])
        else:
            score = random.choice([1, 2, 2, 3])
        
        answers.append({
            "question_id": question_id,
            "question_type": question_type,
            "answer_value": score,
            "answered_at": datetime.now().isoformat()
        })
    return answers


# =============================================================================
# TEST STEPS
# =============================================================================
def step_1_start_session() -> str:
    print_step(1, 6, "Starting Recommendation Session...")
    url = f"{BASE_URL}/career-profile/recommendation/start"
    payload = {"persona_type": "PATHFINDER"}
    
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code not in [200, 201]:
        print_error("Failed to start session", response)
        return None
    
    data = response.json()
    session_token = data.get("session_token")
    if not session_token:
        print_error("No session_token in response", response)
        return None
    
    print_success(f"Session Created! Token: {session_token[:20]}...")
    return session_token


def step_2_submit_riasec(session_token: str) -> dict:
    print_step(2, 6, "Submitting RIASEC Answers...")
    url = f"{BASE_URL}/career-profile/riasec/submit"
    answers = generate_riasec_answers(dominant_types=["I", "R"])
    
    payload = {
        "session_token": session_token,
        "responses": answers
    }
    
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code != 200:
        print_error("Failed to submit RIASEC", response)
        return None
    
    data = response.json()
    riasec_code = data.get("riasec_code", "?")
    print_success(f"RIASEC Submitted! Match Level: {data.get('match_level')} Code: {riasec_code}")
    print_info(f"Top 3 Options: {[c['profession_name'] for c in data.get('top_3_options', [])]}")
    return data


def step_3_start_ikigai(session_token: str) -> list:
    print_step(3, 6, "Starting Ikigai Session (AI Content Generation)...")
    url = f"{BASE_URL}/career-profile/ikigai/start"
    payload = {"session_token": session_token}
    
    print_info("⏳ Waiting for AI Analysis... (this may take 5-30 seconds)")
    start_time = time.time()
    response = requests.post(url, json=payload, headers=HEADERS, timeout=120)
    elapsed = time.time() - start_time
    
    if response.status_code != 200:
        print_error("Failed to start Ikigai", response)
        return None
        
    data = response.json()
    candidates = data.get("candidates_with_content", [])
    print_success(f"Ikigai Content Generated in {elapsed:.2f}s! ({len(candidates)} professions)")
    return candidates


def step_4_submit_ikigai_dimensions(session_token: str, candidates: list) -> dict:
    print_step(4, 6, "Submitting Ikigai Dimensions...")
    url = f"{BASE_URL}/career-profile/ikigai/submit-dimension"
    
    top_profession_id = candidates[0]['profession_id'] if candidates else None
    
    final_result = None
    for i, dim in enumerate(DIMENSION_KEYS):
        print_info(f"Submitting dimension: {dim}")
        payload = {
            "session_token": session_token,
            "dimension_name": dim,
            "selected_profession_id": top_profession_id,
            "selection_type": "selected",
            "reasoning_text": IKIGAI_ESSAYS[dim]
        }
        
        response = requests.post(url, json=payload, headers=HEADERS, timeout=120)
        if response.status_code != 200:
            print_error(f"Failed to submit dimension {dim}", response)
            return None
            
        data = response.json()
        if data.get("all_completed", False) or data.get("status") == "completed":
            final_result = data
            print_success("All dimensions completed! Calculated Result.")
        else:
            print_success(f"Dimension {dim} submitted. Remaining: {data.get('dimensions_remaining')}")
            
    return final_result


def step_5_verify_ikigai_result(session_token: str):
    print_step(5, 6, "Fetching Ikigai Final Result...")
    url = f"{BASE_URL}/career-profile/ikigai/result/{session_token}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
         print_error("Failed to fetch final Ikigai result", response)
         return False
         
    data = response.json()
    top_2 = data.get("top_2_professions", [])
    
    print_success(f"Fetched Top 2 Candidates!")
    for i, c in enumerate(top_2):
        print(f"      {i+1}. Profession ID {c['profession_id']} (Total Score: {c['total_score']:.4f})")
    return True


def main():
    print_header()
    try:
        session_token = step_1_start_session()
        if not session_token: return False
        
        riasec_result = step_2_submit_riasec(session_token)
        if not riasec_result: return False
        
        candidates = step_3_start_ikigai(session_token)
        if not candidates: return False
        
        ikigai_result = step_4_submit_ikigai_dimensions(session_token, candidates)
        if not ikigai_result: return False
        
        success = step_5_verify_ikigai_result(session_token)
        
        print("\n" + "=" * 70)
        if success:
            print("✨ ALL TESTS PASSED SUCCESSFULLY!")
        else:
            print("⚠️  Tests completed with warnings")
        print("=" * 70 + "\n")
        return success
        
    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR!")
        print("   Could not connect to API server.")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
