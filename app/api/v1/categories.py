from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_

from app.database import get_db
from app.crud import category as crud_category
from app.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Список категорий"""
    return await crud_category.get_categories(db)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    """Создание категории"""
    return await crud_category.create_category(db=db, category_in=category_in)

@router.get("/{parent_id}", response_model=list[CategoryResponse])
async def get_categories_by_parent_id(
        parent_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Список категорий по родителям"""
    try:
        categories = await crud_category.get_categories_by_parent(db, parent_id)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occured"
        )
    if categories is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category_by_id(
        category_id: int,
        db: AsyncSession = Depends(get_db)
):
    try:
        category = await crud_category.get_category_by_id(db, category_id)
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

@router.delete("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def delete_category_by_id(category_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление категории"""
    return await crud_category.delete_category_by_id(db, category_id)

@router.patch("/{category_id}", response_model=CategoryUpdate)
async def update_category_by_id(
        category_id: int,
        category_in: CategoryUpdate,
        db: AsyncSession = Depends(get_db)
):
    res = await crud_category.update_category_by_id(db, category_id, category_in)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return res

@router.get("/by-name/{category_name}", response_model=CategoryResponse)
async def get_category_by_name(
        category_name: str,
        db: AsyncSession = Depends(get_db)
):
    try:
        category = await crud_category.get_category_by_name(db, category_name)
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

@router.delete("/by-name/{category_name}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def delete_category_by_name(category_name: str, db: AsyncSession = Depends(get_db)):
    """Удаление категории"""
    return await crud_category.delete_category_by_name(db, category_name)

@router.patch("/by-name/{category_name}", response_model=CategoryUpdate)
async def update_category_by_id(
        category_name: str,
        category_in: CategoryUpdate,
        db: AsyncSession = Depends(get_db)
):
    res = await crud_category.update_category_by_name(db, category_name, category_in)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return res