from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


# Класс для валидации данных пользователя.
class UserSchema(BaseModel):
    email: EmailStr
    fam: str
    name: str
    otc: Optional[str] = None
    phone: str


# Класс для валидации координат перевала.
class CoordSchema(BaseModel):
    latitude: float
    longitude: float
    height: int


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
