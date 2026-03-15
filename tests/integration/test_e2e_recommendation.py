import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_full_recommendation_flow():
    """Test the complete END-TO-END Recommendation Flow"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", timeout=60.0) as client:
        user_id = 'ef9cf8e8-46b1-4e91-89d0-40f6c824319e'
        headers = {"x-user-id": user_id}
        
        # 1. Start Recommendation Session
        response = await client.post("/api/v1/career-profile/recommendation/start", json={
            "persona_type": 'PATHFINDER'
        }, headers=headers)
        assert response.status_code == 200, f"Failed to start session: {response.text}"
        data = response.json()
        session_token = data["session_token"]
        question_ids = data["question_ids"]
        
        # 2. Submit RIASEC responses
        def get_type(q_id):
            if 1 <= q_id <= 12: return "R"
            if 13 <= q_id <= 24: return "I"
            if 25 <= q_id <= 36: return "A"
            if 37 <= q_id <= 48: return "S"
            if 49 <= q_id <= 60: return "E"
            if 61 <= q_id <= 72: return "C"
            return "R"
            
        def get_value(q_type):
            mapping = {"R": 5, "I": 4, "A": 3, "S": 2, "E": 1, "C": 1}
            return mapping.get(q_type, 3)
            
        responses = [
            {
                "question_id": q_id,
                "question_type": get_type(q_id),
                "answer_value": get_value(get_type(q_id)),
                "answered_at": datetime.now(timezone.utc).isoformat()
            }
            for q_id in question_ids
        ]
        
        response = await client.post("/api/v1/career-profile/riasec/submit", json={
            "session_token": session_token,
            "responses": responses
        }, headers=headers)
        assert response.status_code == 200, f"Failed to submit RIASEC: {response.text}"
        
        # 3. Start Ikigai Phase
        response = await client.post("/api/v1/career-profile/ikigai/start", json={
            "session_token": session_token
        }, headers=headers)
        assert response.status_code == 200, f"Failed to start Ikigai: {response.text}"
        ikigai_data = response.json()
        assert "candidates_with_content" in ikigai_data
        candidates = ikigai_data["candidates_with_content"]
        assert len(candidates) > 0
        first_candidate_id = candidates[0]['profession_id']
        
        # 4. Submit Ikigai Dimensions
        dimensions = ["what_you_love", "what_you_are_good_at", "what_the_world_needs", "what_you_can_be_paid_for"]
        
        for i, dim in enumerate(dimensions):
            payload = {
                "session_token": session_token,
                "dimension_name": dim,
                "selected_profession_id": first_candidate_id,
                "selection_type": "selected",
                "reasoning_text": f"This is a detailed reasoning text for the dimension {dim} which requires at least 10 characters."
            }
            response = await client.post("/api/v1/career-profile/ikigai/submit-dimension", json=payload, headers=headers)
            assert response.status_code == 200, f"Failed to submit dimension {dim}: {response.text}"
            dim_resp = response.json()
            
            if i < 3:
                assert "dimension_saved" in dim_resp
            else:
                # The last dimension triggers completion
                assert dim_resp.get("status") == "completed", f"Status not completed: {dim_resp}"
                assert "top_2_professions" in dim_resp
                
        # 5. Fetch Recommendation Result
        response = await client.get(f"/api/v1/career-profile/result/recommendation/{session_token}", headers=headers)
        assert response.status_code == 200, f"Failed to get recommendation result: {response.text}"
        rec_result = response.json()
        
        rec_data = rec_result.get("recommendation", {})
        assert "ikigai_profile_summary" in rec_data
        assert "recommended_professions" in rec_data
        assert len(rec_data["recommended_professions"]) > 0
        
        # 6. Fetch Shared Personality Result
        response = await client.get(f"/api/v1/career-profile/result/personality/{session_token}", headers=headers)
        assert response.status_code == 200, f"Failed to get personality result: {response.text}"
        pers_result = response.json()
        assert pers_result["riasec_code"] is not None
        assert "about_personality" in pers_result
