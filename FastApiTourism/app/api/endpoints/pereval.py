from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.pereval import PerevalCreateSchema
from app.db.repositories.pereval import DatabaseManager
from app.db.database import async_session_maker


router = APIRouter()


# Функция для генерации асинхронных подключений к базе данных.
async def get_async_session():
    async with async_session_maker() as session:
        yield session


# endpoint, добавляющий данные о новом перевале в базу данных.
@router.post("/submit_data")
async def create_pereval(
        pereval: PerevalCreateSchema,
        session: AsyncSession = Depends(get_async_session),
):
    # Преобразовать полученные данные в словарь,
    # используя псевдонимы полей из Pydantic-модели PerevalCreateSchema.
    data = pereval.model_dump(by_alias=True)
    # Создать экземпляр класса для работы с базой данной.
    db_manager = DatabaseManager()
    try:
        # Обработать данные о перевале.
        # Создать экземпляры классов User (если такого пользователя нет), Coord, PerevalAdded, PImage, PerevalImage.
        # Получить и сохранить в переменной id перевала.
        result_id = await db_manager.add_pereval(session, data)
        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "message": None,
                "id": result_id
            }
        )
    # Обработать ошибки входных данных.
    except KeyError as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "message": str(e),
                "id": None
            }
        )
    # Обработать ошибки вызванные SQLAlchemy.
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "message": f"Ошибка подключения к базе данных: {e}",
                "id": None
            }
        )
    # Обработать все остальные ошибки.
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "message": str(e),
                "id": None
            }
        )
