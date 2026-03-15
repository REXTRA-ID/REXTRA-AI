import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_full_fit_check_flow():
    """Test the complete END-TO-END Fit Check Flow"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", timeout=30.0) as client:
        user_id = 'ef9cf8e8-46b1-4e91-89d0-40f6c824319e'
        headers = {"x-user-id": user_id}
        
        response = await client.post("/api/v1/career-profile/fit-check/start", json={
            "persona_type": 'STUDENT',
            "target_profession_id": 1
        }, headers=headers)
        if response.status_code != 200:
            print("FIT CHECK START ERR:", response.text)
        assert response.status_code == 200
        data = response.json()
        session_token = data["session_token"]
        question_ids = data["question_ids"]
        
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
            {"question_id": q_id, "question_type": get_type(q_id), "answer_value": get_value(get_type(q_id)), "answered_at": datetime.now(timezone.utc).isoformat()}
            for q_id in question_ids
        ]
        
        response = await client.post("/api/v1/career-profile/riasec/submit", json={"session_token": session_token, "responses": responses}, headers=headers)
        if response.status_code != 200:
            print("RIASEC SUBMIT ERR:", response.text)
        assert response.status_code == 200
        
        response = await client.get(f"/api/v1/career-profile/result/fit-check/{session_token}", headers=headers)
        if response.status_code != 200:
            print("FIT CHECK RES ERR:", response.text)
        assert response.status_code == 200
        fit_result = response.json()
        
        response = await client.get(f"/api/v1/career-profile/result/personality/{session_token}", headers=headers)
        if response.status_code != 200:
            print("FIT CHECK PERS ERR:", response.text)
        assert response.status_code == 200
