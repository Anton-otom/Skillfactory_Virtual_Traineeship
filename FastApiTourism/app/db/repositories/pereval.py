import base64

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import PerevalAdded, User, Coord, StatusPereval, PerevalImage, PImage


# Класс, реализующий логику работы с базой данных.
class DatabaseManager:

    # Асинхронный метод добавления новых перевалов.
    async def add_pereval(self, session: AsyncSession, pereval_data: dict) -> int:

        # Загрузить в базу данные пользователя (если его нет в базе), добавляющего информацию о перевале.
        user_data = pereval_data.pop('user')
        result = await session.execute(select(User).where(User.email == user_data['email']))
        user = result.scalars().first()
        if not user:
            user = User(**user_data)
            session.add(user)
            await session.flush()  # Получить id пользователя.

        # Загрузить в базу данные координат перевала.
        coord_data = pereval_data.pop('coords')
        coord = Coord(
            latitude=float(coord_data['latitude']),
            longitude=float(coord_data['longitude']),
            height=int(coord_data['height'])
        )
        session.add(coord)
        await session.flush()  # Получить ID координат.

        # Вынести данные об уровне сложности перевала из вложенного словаря "level"
        # в основной словарь "pereval_data".
        level_data = pereval_data.pop('level')
        pereval_data.update({
            'level_winter': level_data.get('winter'),
            'level_summer': level_data.get('summer'),
            'level_autumn': level_data.get('autumn'),
            'level_spring': level_data.get('spring')
        })

        # Убрать информацию о часовом поясе.
        add_time = pereval_data.pop('add_time')
        if add_time.tzinfo is not None:
            add_time = add_time.replace(tzinfo=None)

        # Сохранить изображения перевала в отдельную переменную.
        images_data = pereval_data.pop('images', [])

        # Загрузить в базу данные о перевале.
        pereval = PerevalAdded(
            **pereval_data,
            add_time=add_time,
            creator_id=user.id,
            coord_id=coord.id,
            status=StatusPereval.NEW
        )
        session.add(pereval)
        await session.flush()

        # Сохранить "id" перевала для вывода из метода до закрытия сессии.
        result_pereval_id = pereval.id

        # Преобразовать изображения перевала, если ни в формате "BYTES".
        # Загрузить изображения в базу данных.
        # Привязать изображения к перевалу через таблицу "PerevalImage".
        for img_data in images_data:
            try:
                img_bytes = base64.b64decode(img_data['data'])
            except Exception:
                img_bytes = img_data['data'].encode('utf-8')
            image = PImage(title=img_data['title'], img=img_bytes)
            session.add(image)
            await session.flush()

            pereval_image = PerevalImage(
                pereval_id=pereval.id,
                image_id=image.id
            )
            session.add(pereval_image)

        # Закрыть сессию работы с базой данных.
        await session.commit()
        # Вернуть "id" перевала.
        return result_pereval_id

    # Асинхронный метод получения перевалов по "id".
    async def get_pereval_on_id(self, session: AsyncSession, pereval_id: int) -> PerevalAdded | None:
        # Получить перевал из базы данных, сразу подгрузить значения из связанных моделей.
        result = await session.execute(
            select(PerevalAdded)
            .options(selectinload(PerevalAdded.creator),
                     selectinload(PerevalAdded.coords),
                     selectinload(PerevalAdded.images).selectinload(PerevalImage.image))
            .where(PerevalAdded.id == pereval_id))
        pereval_data = result.scalars().first()

        # Если перевала с запрашиваемым "id" нет, вернуть "None", если вернуть объект перевала.
        if not pereval_data:
            return None
        return pereval_data
