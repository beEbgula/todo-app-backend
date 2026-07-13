from sqlalchemy.orm import Session

from app.repositories.task import TaskRepo
from app.schemas.taskSC import CreateTaskSCHEMA, TaskSCHEMA, UpdateTaskSCHEMA


class TaskNotFound(Exception):
    """Задача не найдена"""


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repo = TaskRepo(db)


    def list_tasks(self) -> list[TaskSCHEMA]:
        tasks_orm = self.task_repo.get_all()
        return [TaskSCHEMA.model_validate(task) for task in tasks_orm]


    def create_task(self, create_task: CreateTaskSCHEMA) -> TaskSCHEMA:
        task = self.task_repo.create(title=create_task.title)
        self.db.commit()
        return TaskSCHEMA.model_validate(task)
    

    def update_task(self, task_id: str, update_task: UpdateTaskSCHEMA) -> TaskSCHEMA:
        task_for_update = self.task_repo.get_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")

        if update_task.title is not None:
            task_for_update.title = update_task.title
        if update_task.completed is not None:
            task_for_update.completed = update_task.completed
        self.db.commit()
        return TaskSCHEMA.model_validate(task_for_update)


    def delete_task(self, task_id: str) -> None:
        task_for_delete = self.task_repo.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        self.task_repo.delete(task_for_delete)
        self.db.commit()


