from sqlalchemy import select, delete
from sqlalchemy.engine import result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from sqlalchemy.orm import query
from sqlalchemy.testing import exclude

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse


async def get_categories(db: AsyncSession) -> List[Category]:
    get_result = await db.execute(select(Category))
    return get_result.scalars().all()

async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    get_result = await db.execute(select(Category).where(Category.id == category_id))
    return get_result.scalars().first()

async def create_category(db: AsyncSession, category_in: CategoryCreate) -> Category:
    db_category = Category(name=category_in.name, parent_id=category_in.parent_id)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def delete_category(db: AsyncSession, category_id: int) -> Category | None:
    query = select(Category).where(Category.id == category_id)
    delete_result = await db.execute(query)
    category = delete_result.scalars().first()

    if not category:
        return None

    await db.delete(category)
    await db.commit()

    return category

async def update_category(db: AsyncSession, category_id: int, category_in: CategoryResponse) -> Category | None:
    query = select(Category).where(Category.id == category_id)
    update_result = await db.execute(query)
    db_category = update_result.scalars().first()

    if not db_category:
        return None
    update_data = category_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_category, key, value)

    await db.commit()
    await db.refresh(db_category)

    return db_category