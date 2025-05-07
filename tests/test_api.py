import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from main import app
from app.db.repositories.pereval import DatabaseManager

@pytest.mark.asyncio
async def test_api_crud(client, sample_pereval_json):
    # Мокаем DatabaseManager и его методы
    mock_db_manager = AsyncMock()
    mock_db_manager.add_pereval.return_value = 123

    pereval_obj = MagicMock()
    pereval_obj.title = "Пхия"
    pereval_obj.creator = MagicMock()
    pereval_obj.creator.email = "qwerty@mail.ru"
    pereval_obj.coords = MagicMock()
    pereval_obj.coords.latitude = 45.3842
    mock_db_manager.get_pereval_on_id.return_value = pereval_obj

    # Для поиска по email
    mock_db_manager.get_perevals_on_email.return_value = [pereval_obj]

    # Для patch
    mock_db_manager.patch_pereval_on_id.return_value = (1, "Данные перевала успешно обновлены.")

    app.dependency_overrides[DatabaseManager] = lambda: mock_db_manager

    # 1. Добавить перевал
    response = client.post("/submit_data", json=sample_pereval_json)
    assert response.status_code == 200
    assert response.json().get("id") == 123

    # 2. Получить перевал по id
    response = client.get("/submit_data/123/")
    assert response.status_code == 200
    result = response.json()
    assert result["title"] == "Пхия"
    assert result["user"]["email"] == "qwerty@mail.ru"
    assert float(result["coords"]["latitude"]) == 45.3842

    # 3. Получить перевалы по email
    response = client.get("/submit_data/?user__email=qwerty@mail.ru")
    assert response.status_code == 200
    perevals = response.json()
    assert isinstance(perevals, list)
    assert perevals[0]["title"] == "Пхия"

    # 4. Изменить перевал (patch)
    patch_data = {"title": "Пхия (обновлено)"}
    response = client.patch("/submit_data/123/", json=patch_data)
    assert response.status_code == 200
    assert "успешно" in response.json().get("message", "").lower()
