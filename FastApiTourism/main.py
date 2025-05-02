from fastapi import FastAPI
from app.api.endpoints.pereval import router as pereval_router

app = FastAPI()
app.include_router(pereval_router)
