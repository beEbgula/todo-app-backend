from pydantic import BaseModel, ConfigDict


class CategorySCHEMA(BaseModel):
    id: str
    name: str
    model_config = ConfigDict(from_attributes=True)

class CreateCategorySCHEMA(BaseModel):
    name: str

class UpdateCategorySCHEMA(BaseModel):
    name: str | None = None

class DeleteCategorySchema(BaseModel):
    id: str
