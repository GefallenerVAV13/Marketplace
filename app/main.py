from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_async_session

app = FastAPI(title="Marketplace API")


@app.get("/")
async def root():
    return {"message": "Marketplace API is running!"}


@app.get("/healthcheck")
async def healthcheck(db: AsyncSession = Depends(get_async_session)):
    # Выполняем простой запрос к БД для проверки связи
    result = await db.execute(text("SELECT 1"))
    return {"database": "connected", "result": result.scalar()}