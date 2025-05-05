import base64

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.pereval import (
    PerevalCreateSchema,
    PerevalReadSchema,
    CoordSchema,
    UserSchema,
    ImageSchema,
    PerevalUpdateSchema
)
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


# endpoint, возвращающий данные о перевале по "id".
@router.get("/submit_data/{id}", response_model=PerevalReadSchema)
async def get_pereval_on_id(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    # Создать экземпляр класса для работы с базой данной.
    db_manager = DatabaseManager()
    try:
        # Получить перевал по запрашиваемому "id".
        # Если такого "id" нет, вызвать "ValueError"
        pereval = await db_manager.get_pereval_on_id(session, id)
        if pereval is None:
            raise ValueError
        # Преобразовать экземпляр класса в Pydantic-схему и вернуть её.
        return PerevalReadSchema(
            status=pereval.status,
            beauty_title=pereval.beauty_title,
            title=pereval.title,
            other_titles=pereval.other_titles,
            connect=pereval.connect,
            add_time=pereval.add_time,
            user=UserSchema(
                email=pereval.creator.email,
                fam=pereval.creator.fam,
                name=pereval.creator.name,
                otc=pereval.creator.otc,
                phone=pereval.creator.phone,
            ),
            coords=CoordSchema(
                latitude=pereval.coords.latitude,
                longitude=pereval.coords.longitude,
                height=pereval.coords.height,
            ),
            level_winter=pereval.level_winter,
            level_summer=pereval.level_summer,
            level_autumn=pereval.level_autumn,
            level_spring=pereval.level_spring,
            images=[
                ImageSchema(
                    data=base64.b64encode(
                        img.image.img.encode('utf-8')
                        if isinstance(img.image.img, str)
                        else img.image.img
                    )
                    .decode("utf-8"),
                    title=img.image.title
                ) for img in pereval.images
            ]
        )
    # Обработать ошибку отсутствия перевала с запрашиваемым "id".
    except ValueError as e:
        print('Чек ValueError')
        return JSONResponse(
            status_code=404,
            content={
                "status": 404,
                "message": f"Перевал с id {id} в базе отсутствует. {str(e)}"
            }
        )
    # Обработать все остальные ошибки.
    except Exception as e:
        print('Чек Exception')
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "message": str(e)
            }
        )


# endpoint, изменяющий данные о перевале по "id".
@router.patch("/submit_data/{id}", response_model=PerevalReadSchema)
async def patch_pereval_on_id(
        id: int,
        pereval: PerevalUpdateSchema,
        session: AsyncSession = Depends(get_async_session),
):
    # Создать экземпляр класса для работы с базой данной.
    db_manager = DatabaseManager()
    try:
        # Преобразовать Pydantic-схему в словарь.
        patch_pereval = pereval.model_dump(exclude_unset=True, by_alias=True)
        # Удалить поле "user", если оно было передано.
        patch_pereval.pop("user", None)
        # Выполнить поиск перевала в базе данных.
        # Получить код результата и сообщение.
        # Если код "1" - перевал найден и изменён. Сообщение "None".
        # Если код "0" - перевал не найден или не обновлён. Сообщение с причиной ошибки.
        state, message = await db_manager.patch_pereval_on_id(session, id, patch_pereval)
        return JSONResponse(
            status_code=200 if state else 400,
            content={"state": state, "message": message}
        )
    # Обработать ошибку валидации.
    except ValidationError as e:
        print('Чек ValueError')
        return JSONResponse(
            status_code=422,
            content={"state": 0, "message": f"Ошибка валидации: {e.errors()}"}
        )
    # Обработать все остальные ошибки.
    except Exception as e:
        print('Чек Exception')
        return JSONResponse(
            status_code=500,
            content={"state": 0, "message": f"Ошибка сервера: {str(e)}"}
        )
