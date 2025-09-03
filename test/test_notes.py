import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture
async def token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Регистрация пользователя для теста
        await ac.post("/auth/register", json={"username": "noteuser", "password": "pass1234"})
        # Вход для получения токена
        response = await ac.post("/auth/login", data={"username": "noteuser", "password": "pass1234"})
        token_data = response.json()
        return token_data["access_token"]

@pytest.mark.asyncio
async def test_create_read_update_delete_note(token):
    headers = {"Authorization": f"Bearer {token}"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Создаем заметку
        create_response = await ac.post(
            "/notes/",
            json={"title": "Test Note", "content": "Content of the note"},
            headers=headers
        )
        assert create_response.status_code == 200
        note = create_response.json()
        note_id = note["id"]
        assert note["title"] == "Test Note"

        list_response = await ac.get("/notes/", headers=headers)
        assert list_response.status_code == 200
        notes = list_response.json()
        assert any(n["id"] == note_id for n in notes)

        get_response = await ac.get(f"/notes/{note_id}", headers=headers)
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "Test Note"

        update_response = await ac.put(
            f"/notes/{note_id}",
            json={"title": "Updated Title", "content": "Updated Content"},
            headers=headers
        )
        assert update_response.status_code == 200
        updated_note = update_response.json()
        assert updated_note["title"] == "Updated Title"

        delete_response = await ac.delete(f"/notes/{note_id}", headers=headers)
        assert delete_response.status_code == 200
        assert delete_response.json()["detail"] == "Note deleted"

        get_after_delete = await ac.get(f"/notes/{note_id}", headers=headers)
        assert get_after_delete.status_code == 404
