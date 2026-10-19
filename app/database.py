from sqlalchemy.ext.asyncio import create_async_engine, async_session, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declarative_base

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL_async, echo = True)

async_session_marker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

import app.models

async def get_db() -> AsyncSession:
    """Генератор сессий для эндпоинтов"""
    async with async_session_marker() as session:
        yield session

# async def get_async_session():
#     async with async_session_marker() as session:
#         yield session