import base64

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import PerevalAdded, User, Coord, StatusPereval, PerevalImage, PImage


class DatabaseManager:

    async def add_pereval(self, session: AsyncSession, pereval_data: dict) -> int:
        # Создаем пользователя
        user_data = pereval_data.pop('user')
        result = await session.execute(select(User).where(User.email == user_data['email']))
        user = result.scalars().first()
        if not user:
            user = User(**user_data)
            session.add(user)
            await session.flush()  # Получаем id пользователя

        # Создаем координаты
        coord_data = pereval_data.pop('coords')
        coord = Coord(
            latitude=float(coord_data['latitude']),
            longitude=float(coord_data['longitude']),
            height=int(coord_data['height'])
        )
        session.add(coord)
        await session.flush()  # Получаем ID координат

        # Обрабатываем уровень сложности
        level_data = pereval_data.pop('level')
        pereval_data.update({
            'level_winter': level_data.get('winter'),
            'level_summer': level_data.get('summer'),
            'level_autumn': level_data.get('autumn'),
            'level_spring': level_data.get('spring')
        })

        # (отбрасываем информацию о таймзоне)
        add_time = pereval_data.pop('add_time')
        if add_time.tzinfo is not None:
            add_time = add_time.replace(tzinfo=None)

        images_data = pereval_data.pop('images', [])

        # Создаем перевал
        pereval = PerevalAdded(
            **pereval_data,
            add_time=add_time,
            creator_id=user.id,
            coord_id=coord.id,
            status=StatusPereval.NEW
        )
        session.add(pereval)
        await session.flush()
        result_pereval_id = pereval.id

        # Добавляем изображения
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

        await session.commit()
        return result_pereval_id
