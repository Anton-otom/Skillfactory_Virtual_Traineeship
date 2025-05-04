from datetime import datetime
from enum import IntEnum
from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_serializer, ConfigDict


# Класс для валидации данных пользователя.
class UserSchema(BaseModel):
    email: EmailStr
    fam: str
    name: str
    otc: Optional[str] = None
    phone: str
    # Параметр для автоматического преобразования ORM в Pydantic.
    model_config = ConfigDict(from_attributes=True)


# Класс для валидации координат перевала.
class CoordSchema(BaseModel):
    latitude: float
    longitude: float
    height: int
    # Параметр для автоматического преобразования ORM в Pydantic.
    model_config = ConfigDict(from_attributes=True)


# Класс для валидации уровней сложности перевала в разные времена года.
class LevelSchema(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


# Класс для валидации изображений.
class ImageSchema(BaseModel):
    data: str
    title: str
    # Параметр для автоматического преобразования ORM в Pydantic.
    model_config = ConfigDict(from_attributes=True)


# Класс для валидации всех входных данных.
# Данные по ключам "beauty_title", "title", "other_titles",
# "connect, "add_time" проверяются напрямую.
# Данные по ключам "user", "coords", "level", "images"
# проверяются с помощью вложенных классов валидации.
class PerevalCreateSchema(BaseModel):
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime
    user: UserSchema
    coords: CoordSchema
    level: LevelSchema
    images: List[ImageSchema]


# Класс для преобразования числовых статусов в удобные для восприятия пользователем.
class StatusPerevalEnum(IntEnum):
    NEW = 1
    PENDING = 2
    ACCEPTED = 3
    REJECTED = 4

    def __str__(self):
        return {
            1: "Ожидает модерации",
            2: "На модерации",
            3: "Принят",
            4: "Отклонён"
        }[self.value]


# Класс для валидации данных о перевале, получаемых из базы данных.
class PerevalReadSchema(BaseModel):
    status: StatusPerevalEnum
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime
    user: UserSchema
    coords: CoordSchema
    level_winter: Optional[str] = None
    level_summer: Optional[str] = None
    level_autumn: Optional[str] = None
    level_spring: Optional[str] = None
    images: List[ImageSchema]

    # Параметр для автоматического преобразования ORM в Pydantic.
    model_config = ConfigDict(from_attributes=True)

    # Метод для преобразования числовых статусов в удобные для восприятия пользователем.
    @field_serializer("status")
    def serialize_status(self, status):
        return str(status)
