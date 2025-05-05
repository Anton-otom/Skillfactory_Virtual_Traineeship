from datetime import datetime
from enum import IntEnum
from typing import List
from pydantic import BaseModel, EmailStr, field_serializer, ConfigDict


# Класс для валидации данных пользователя.
class UserSchema(BaseModel):
    email: EmailStr
    fam: str
    name: str
    otc: str | None = None
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
    winter: str | None = None
    summer: str | None = None
    autumn: str | None = None
    spring: str | None = None


# Класс для валидации изображений.
class ImageSchema(BaseModel):
    data: str
    title: str
    # Параметр для автоматического преобразования ORM в Pydantic.
    model_config = ConfigDict(from_attributes=True)


# Класс для валидации входных данных, получаемых при создании перевала.
# Данные по ключам "beauty_title", "title", "other_titles",
# "connect, "add_time" проверяются напрямую.
# Данные по ключам "user", "coords", "level", "images"
# проверяются с помощью вложенных классов валидации.
class PerevalCreateSchema(BaseModel):
    beauty_title: str
    title: str
    other_titles: str | None = None
    connect: str | None = None
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
    other_titles: str | None = None
    connect: str | None = None
    add_time: datetime
    user: UserSchema
    coords: CoordSchema
    level_winter: str | None = None
    level_summer: str | None = None
    level_autumn: str | None = None
    level_spring: str | None = None
    images: List[ImageSchema]

    # Параметр для автоматического преобразования ORM в Pydantic.
    model_config = ConfigDict(from_attributes=True)

    # Метод для преобразования числовых статусов в удобные для восприятия пользователем.
    @field_serializer("status")
    def serialize_status(self, status):
        return str(status)


# Класс для валидации входных данных, получаемых при изменении информации о перевале.
class PerevalUpdateSchema(PerevalCreateSchema):
    # Запретить поля неуказанные в этом классе.
    model_config = ConfigDict(extra="forbid")

    # Исключить поле с данными пользователя.
    user: None = None

    # Сделать все остальные поля необязательными.
    beauty_title: str | None = None
    title: str | None = None
    other_titles: str | None = None
    connect: str | None = None
    add_time: datetime | None = None
    coords: CoordSchema | None = None
    level: LevelSchema | None = None
    images: list[ImageSchema] | None = None