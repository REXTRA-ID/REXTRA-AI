import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_complete_riasec_flow():
    """Test complete RIASEC flow"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Start test
        response = await client.post("/api/v1/career-profile/start", json={
            "user_id": 'ef9cf8e8-46b1-4e91-89d0-40f6c824319e'
        })
        assert response.status_code == 200
        data = response.json()
        session_token = data["session_token"]
        questions = data["questions"]
        assert len(questions) == 72
        
        # 2. Submit RIASEC responses
        responses = {str(i): 4 for i in range(1, 73)}  # All 4s
        
        response = await client.post("/api/v1/career-profile/riasec/submit", json={
            "session_token": session_token,
            "responses": responses
        })
        assert response.status_code == 200
        result = response.json()
        
        assert "riasec_code" in result
        assert "riasec_scores" in result
        assert "code_details" in result
        
        # 3. Get result
        response = await client.get(f"/api/v1/career-profile/riasec/result/{session_token}")
        assert response.status_code == 200
        result = response.json()
        
        assert result["riasec_code"] is not None
        assert len(result["riasec_scores"]) == 6  # R, I, A, S, E, C
