from fastapi import FastAPI
from app.api.endpoints.pereval import router as pereval_router

# Создать приложение
app = FastAPI()
# Подключить к приложению пути, обрабатывающие запросы о перевалах
app.include_router(pereval_router)
