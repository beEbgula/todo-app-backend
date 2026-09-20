from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.database.session import get_db
from app.services.category import CategoryService
from app.services.task import TaskService


"""Функция для инъекции зависимости TaskService"""
def get_task_service(
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
    ) -> TaskService:
    return TaskService(
        db,
        cache_redis_url=settings.REDIS_URL,
        cache_ttl_seconds=settings.CACHE_TTL_SECONDS,
        cache_tasks_key=settings.CACHE_TASKS_KEY,
        )
    
"""Функция для инъекции зависимости CatogoryService"""
def get_category_service(
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
    ) -> CategoryService:
    return CategoryService(
        db,
        cache_redis_url=settings.REDIS_URL,
        cache_ttl_seconds=settings.CACHE_TTL_SECONDS,
        cache_categories_key=settings.CACHE_CATEGORIES_KEY,
        )
