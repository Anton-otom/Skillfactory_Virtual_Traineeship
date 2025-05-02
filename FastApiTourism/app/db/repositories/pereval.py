from sqlalchemy.orm import Session

from app.db.models import PerevalAdded, User, Coord, StatusPereval, PerevalImage, PImage


class DatabaseManager:
    def __init__(self, session: Session):
        self.session = session

    def add_pereval(self, pereval_data: dict) -> PerevalAdded:
        # Создаем пользователя
        user_data = pereval_data.pop('user')
        user = self.session.query(User).filter_by(email=user_data['email']).first()
        if not user:
            user = User(**user_data)
            self.session.add(user)
            self.session.flush()  # Получаем id пользователя

        # Создаем координаты
        coord_data = pereval_data.pop('coords')
        coord = Coord(
            latitude=float(coord_data['latitude']),
            longitude=float(coord_data['longitude']),
            height=int(coord_data['height'])
        )
        self.session.add(coord)
        self.session.flush()  # Получаем ID координат

        # Обрабатываем уровень сложности
        level_data = pereval_data.pop('level')
        pereval_data.update({
            'level_winter': level_data.get('winter'),
            'level_summer': level_data.get('summer'),
            'level_autumn': level_data.get('autumn'),
            'level_spring': level_data.get('spring')
        })

        # Создаем перевал
        pereval = PerevalAdded(
            **pereval_data,
            coord_id=coord.id,
            user_id=user.id,
            status=StatusPereval.NEW
        )
        self.session.add(pereval)
        self.session.flush()

        # Добавляем изображения
        for img_data in pereval_data.get('images'):
            image = PerevalImage(
                pereval_id=pereval.id,
                image=PImage(title=img_data['title'], img=img_data['data'])
            )
            self.session.add(image)

        self.session.commit()
        return pereval
