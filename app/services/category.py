from sqlalchemy.orm import Session

from app.repositories.category import CatergoryRepo
from app.schemas.categorySC import CategorySCHEMA, CreateCategorySCHEMA, UpdateCategorySCHEMA


class CategoryNotFound(Exception):
    """Категория не найдена"""


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repo = CatergoryRepo(db)


    def list_categories(self) -> list[CategorySCHEMA]:
        category_orm = self.category_repo.get_all()
        return [CategorySCHEMA.model_validate(category) for category in category_orm]


    def create_category(self, create_category: CreateCategorySCHEMA) -> CategorySCHEMA:
        category = self.category_repo.create(name=create_category.name)
        self.db.commit()
        return CategorySCHEMA.model_validate(category)


    def update_category(self, category_id: str, update_category: UpdateCategorySCHEMA) -> CategorySCHEMA:
        category_for_update = self.category_repo.get_by_id(category_id=category_id)
        if not category_for_update:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")        
        
        if update_category.name is not None:
            category_for_update.name = update_category.name
        self.db.commit()
        return CategorySCHEMA.model_validate(category_for_update)


    def delete_category(self, category_id: str) -> CategorySCHEMA:
        category_for_delete = self.category_repo.get_by_id(category_id=category_id)
        if not category_for_delete:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")
        self.category_repo.delete(category_for_delete)
        self.db.commit()