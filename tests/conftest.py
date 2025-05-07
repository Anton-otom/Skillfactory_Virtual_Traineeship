from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Фикстура для тестового клиента FastAPI."""
    return TestClient(app)

@pytest.fixture
def sample_pereval_json():
    """Пример входных данных для создания перевала."""
    return {
        "beauty_title": "пер. ",
        "title": "Пхия",
        "other_titles": "Триев",
        "connect": "",
        "add_time": datetime.strptime("2021-09-22 13:18:13", "%Y-%m-%d %H:%M:%S"),
        "user": {
            "email": "qwerty@mail.ru",
            "fam": "Иванов",
            "name": "Василий",
            "otc": "Иванович",
            "phone": "+7 555 55 55"
        },
        "coords": {
            "latitude": "45.3842",
            "longitude": "7.1525",
            "height": "1200"
        },
        "level": {
            "winter": "",
            "summer": "1А",
            "autumn": "1А",
            "spring": ""
        },
        "images": [
            {"data": "aGVsbG8=", "title": "Седловина"},
            {"data": "d29ybGQ=", "title": "Подъём"}
        ]
    }