from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    fam: str
    name: str
    otc: Optional[str] = None
    phone: str


class CoordSchema(BaseModel):
    latitude: float
    longitude: float
    height: int


class LevelSchema(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


class ImageSchema(BaseModel):
    data: str
    title: str


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
