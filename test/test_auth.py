import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/register",
            json={"username": "testuser", "password": "testpass123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert "id" in data

        response_duplicate = await ac.post(
            "/auth/register",
            json={"username": "testuser", "password": "testpass123"}
        )
        assert response_duplicate.status_code == 400

        login_response = await ac.post(
            "/auth/login",
            data={"username": "testuser", "password": "testpass123"}
        )
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

        bad_login_response = await ac.post(
            "/auth/login",
            data={"username": "testuser", "password": "wrongpassword"}
        )
        assert bad_login_response.status_code == 401
