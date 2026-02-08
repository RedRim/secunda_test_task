"""
настройка подключения к базе данных
"""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer

from app.config import get_config

DATABASE_URL = get_config().db.dsn

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """
    базовый класс для всех моделей
    """


async def get_session():
    """
    генератор сессий для dependency injection
    """
    async with async_session_maker() as session:
        yield session
