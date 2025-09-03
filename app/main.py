from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.config import settings
import logging

from app.api import auth, notes
from app.db import database

# Инициализация логирования
import core.logging
logger = core.logging.logger

app = FastAPI(title=settings.PROJECT_NAME)

# Middleware для CORS (по необходимости)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение к базе данных при запуске
@app.on_event("startup")
async def startup():
    await database.connect()
    logger.info("Connected to database")

# Отключение базы при завершении
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.info("Disconnected from database")

# Включение маршрутов
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
