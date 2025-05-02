from datetime import datetime
from enum import IntEnum
from sqlalchemy import (
    Integer,
    String,
    Numeric,
    ForeignKey,
    TIMESTAMP,
    text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import BYTEA

from app.db.database import Base


# Пользовательский тип ENUM
class StatusPereval(IntEnum):
    NEW = 1
    PENDING = 2
    ACCEPTED = 3
    REJECTED = 4


# Модель пользователей
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    fam: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    otc: Mapped[str] = mapped_column(String(255), nullable=True)


# Модель координат
class Coord(Base):
    __tablename__ = "coords"

    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)
    longitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)


# Модель перевалов
class PerevalAdded(Base):
    __tablename__ = "pereval_added"

    id: Mapped[int] = mapped_column(primary_key=True)
    beauty_title: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    other_titles: Mapped[str] = mapped_column(String(255), nullable=True)
    connect: Mapped[str] = mapped_column(String(255), nullable=True)
    add_time: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("NOW()"))
    coord_id: Mapped[int] = mapped_column(ForeignKey("coords.id"), nullable=False)
    level_winter: Mapped[str] = mapped_column(String(6), nullable=True)
    level_summer: Mapped[str] = mapped_column(String(6), nullable=True)
    level_autumn: Mapped[str] = mapped_column(String(6), nullable=True)
    level_spring: Mapped[str] = mapped_column(String(6), nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=StatusPereval.NEW)

    coords: Mapped["Coord"] = relationship()
    images: Mapped[list["PerevalImage"]] = relationship(back_populates="pereval")


# Модель изображений
class PImage(Base):
    __tablename__ = "p_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    img: Mapped[bytes] = mapped_column(BYTEA, nullable=False)


# Связующая таблица перевал-изображение
class PerevalImage(Base):
    __tablename__ = "pereval_images"

    pereval_id: Mapped[int] = mapped_column(ForeignKey("pereval_added.id"), primary_key=True)
    image_id: Mapped[int] = mapped_column(ForeignKey("p_images.id"), primary_key=True)
    date_added: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("NOW()"))

    pereval: Mapped["PerevalAdded"] = relationship(back_populates="images")
    image: Mapped["PImage"] = relationship()


# Модель областей
class PerevalArea(Base):
    __tablename__ = "pereval_areas"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_parent: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)


# Модель типов активностей
class SprActivitiesType(Base):
    __tablename__ = "spr_activities_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
