from pydantic import BaseModel, ConfigDict


class TaskSCHEMA(BaseModel):
    id: str
    title: str
    completed: bool
    model_config = ConfigDict(from_attributes=True)


class CreateTaskSCHEMA(BaseModel):
    title: str

class UpdateTaskSCHEMA(BaseModel):
    title: str | None = None
    completed: bool | None = None

class DeleteTaskSCHEMA(BaseModel):
    id: str