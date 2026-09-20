from sqlalchemy.orm import Session

from app.api.cache.redis import RedisCacheBackend
from app.repositories.category import CatergoryRepo
from app.schemas.categorySC import CategorySCHEMA, CreateCategorySCHEMA, UpdateCategorySCHEMA


class CategoryNotFound(Exception):
    """Категория не найдена"""


class CategoryService:
    def __init__(self,
     db: Session,
     cache_redis_url: str,
     cache_ttl_seconds: int,
     cache_categories_key: str,
     ) -> None:
        self.db = db
        self.category_repo = CatergoryRepo(db)
        self.cache = RedisCacheBackend(cache_redis_url, cache_ttl_seconds)
        self.cache_categories_key = cache_categories_key



    def list_categories(self) -> list[CategorySCHEMA]:
        #Шаг 1: проверка на данные в Redis
        cached_categories = self.cache.get(self.cache_categories_key)
        if cached_categories is not None:
            return cached_categories
            
        category_orm = self.category_repo.get_all()

        category_read = [CategorySCHEMA.model_validate(category) for category in category_orm]
        categories_for_cache = [category.model_dump() for category in category_read]
        self.cache.set(self.cache_categories_key, categories_for_cache)

        return category_read


    def create_category(self, create_category: CreateCategorySCHEMA) -> CategorySCHEMA:
        self.cache.delete(self.cache_categories_key)

        category = self.category_repo.create(name=create_category.name)
        self.db.commit()
        return CategorySCHEMA.model_validate(category)


    def update_category(self, category_id: str, update_category: UpdateCategorySCHEMA) -> CategorySCHEMA:
        self.cache.delete(self.cache_categories_key)

        category_for_update = self.category_repo.get_by_id(category_id=category_id)
        if not category_for_update:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")        
        
        if update_category.name is not None:
            category_for_update.name = update_category.name
        self.db.commit()
        return CategorySCHEMA.model_validate(category_for_update)


    def delete_category(self, category_id: str) -> CategorySCHEMA:
        self.cache.delete(self.cache_categories_key)

        category_for_delete = self.category_repo.get_by_id(category_id=category_id)
        if not category_for_delete:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")
        self.category_repo.delete(category_for_delete)
        self.db.commit()