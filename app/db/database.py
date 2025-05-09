from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Создать движок базы данных
engine = create_async_engine(settings.async_database_url)
# Передать движок в генератор асинхронных сессий
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


# Базовый класс для всех моделей базы данных
class Base(DeclarativeBase):
    pass
