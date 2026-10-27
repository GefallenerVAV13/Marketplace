from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_

from app.database import get_db
from app.crud import category as crud_category
from app.schemas.category import CategoryResponse, CategoryCreate

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Список категорий"""
    return await crud_category.get_categories(db)

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
        category_id: int,
        db: AsyncSession = Depends(get_db)
):
    try:
        category = await crud_category.get_category(db, category_id)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occured"
        )
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    """Создание категории"""
    return await crud_category.create_category(db=db, category_in=category_in)

@router.delete("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление категории"""
    return await crud_category.delete_category(db, category_id)

@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
        category_id: int,
        category_in: CategoryResponse,
        db: AsyncSession = Depends(get_db)
):
    update_category = await crud_category.update_category(db, category_id, category_in)

    if not update_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return update_category