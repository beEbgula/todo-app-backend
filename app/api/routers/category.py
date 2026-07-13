from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_category_service
from app.schemas.categorySC import CategorySCHEMA, CreateCategorySCHEMA, UpdateCategorySCHEMA
from app.services.category import CategoryNotFound, CategoryService


router = APIRouter(prefix="/categories")


@router.get("")
def read_categories(
    category_service: CategoryService = Depends(get_category_service)
    ) -> list[CategorySCHEMA]:
    return category_service.list_categories()

    
@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CreateCategorySCHEMA,
    category_service: CategoryService = Depends(get_category_service)
    ) -> CategorySCHEMA:
    return category_service.create_category(create_category=payload)


@router.patch("/{category_id}")
def update_category(
    category_id: str,
    payload: UpdateCategorySCHEMA,
    category_service: CategoryService = Depends(get_category_service)
    ) -> CategorySCHEMA:
    try:
        return category_service.update_category(category_id=category_id, update_category=payload)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service)) -> None:
    try:
        return category_service.delete_category(category_id=category_id)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)