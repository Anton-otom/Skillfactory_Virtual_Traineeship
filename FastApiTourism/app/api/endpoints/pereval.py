from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.pereval import PerevalCreateSchema
from app.db.repositories.pereval import DatabaseManager
from app.db.database import async_session_maker


router = APIRouter()


async def get_session():
    async with async_session_maker() as session:
        yield session


@router.post("/submit_data")
async def create_pereval(
        pereval: PerevalCreateSchema,
        session: AsyncSession = Depends(get_session),
):
    data = pereval.model_dump(by_alias=True)
    db_manager = DatabaseManager()
    try:
        result_id = await db_manager.add_pereval(session, data)
        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "message": None,
                "id": result_id
            }
        )
    except KeyError as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "message": str(e),
                "id": None
            }
        )
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "message": f"Ошибка подключения к базе данных: {e}",
                "id": None
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "message": str(e),
                "id": None
            }
        )
