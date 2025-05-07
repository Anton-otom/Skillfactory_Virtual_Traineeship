import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.db.repositories.pereval import DatabaseManager
from app.db.models import StatusPereval

@pytest.mark.asyncio
async def test_add_get_patch_pereval(sample_pereval_json):
    db = DatabaseManager()
    session = AsyncMock()

    # Мокаем select(User).where(User.email == ...)
    user_mock = MagicMock()
    user_mock.id = 1
    session.execute.return_value.scalars.return_value.first.side_effect = [None, user_mock, user_mock]
    session.flush = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()

    with patch("app.db.models.User", autospec=True) as MockUser, \
         patch("app.db.models.Coord", autospec=True) as MockCoord, \
         patch("app.db.models.PerevalAdded", autospec=True) as MockPerevalAdded, \
         patch("app.db.models.PImage", autospec=True) as MockPImage, \
         patch("app.db.models.PerevalImage", autospec=True):

        mock_user = MockUser.return_value
        mock_user.id = 1
        mock_coord = MockCoord.return_value
        mock_coord.id = 2
        mock_pereval = MockPerevalAdded.return_value
        mock_pereval.id = 3

        # Добавление перевала
        new_id = await db.add_pereval(session, sample_pereval_json.copy())
        assert new_id == 3

        # Получение перевала по id
        mock_pereval.title = "Пхия"
        mock_pereval.creator = mock_user
        mock_pereval.coords = mock_coord
        session.execute.return_value.scalars.return_value.first.return_value = mock_pereval

        pereval_obj = await db.get_pereval_on_id(session, 3)
        assert pereval_obj.title == "Пхия"
        assert pereval_obj.creator.id == 1

        # Получение перевалов по email
        session.execute.return_value.scalars.side_effect = [
            MagicMock(first=MagicMock(return_value=mock_user)),  # user
            MagicMock(all=MagicMock(return_value=[mock_pereval]))  # perevals
        ]
        perevals = await db.get_perevals_on_email(session, "qwerty@mail.ru")
        assert isinstance(perevals, list)
        assert perevals[0].title == "Пхия"

        # Частичное обновление (patch)
        mock_pereval.status = StatusPereval.NEW
        session.execute.return_value.scalars.return_value.first.return_value = mock_pereval
        code, msg = await db.patch_pereval_on_id(session, 3, {"title": "Пхия (обновлено)"})
        assert code in (1, 0)
