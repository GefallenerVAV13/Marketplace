from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.category import Category
from app.schemas.category import CategoryCreate


async def get_categories(db: AsyncSession) -> List[Category]:
    result = await db.execute(select(Category))
    return result.scalars().all()

async def create_category(db: AsyncSession, category_in: CategoryCreate) -> Category:
    db_category = Category(name=category_in.name, parent_id=category_in.parent_id)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category