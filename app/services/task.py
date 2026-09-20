from sqlalchemy.orm import Session

from app.api.cache.redis import RedisCacheBackend
from app.repositories.task import TaskRepo
from app.schemas.taskSC import CreateTaskSCHEMA, TaskSCHEMA, UpdateTaskSCHEMA


class TaskNotFound(Exception):
    """Задача не найдена"""


class TaskService:
    def __init__(self,
    db: Session,
    cache_redis_url: str,
    cache_ttl_seconds: int,
    cache_tasks_key: str,
    ) -> None:
        self.db = db
        self.task_repo = TaskRepo(db)
        self.cache = RedisCacheBackend(cache_redis_url, cache_ttl_seconds)
        self.cache_tasks_key = cache_tasks_key

    def list_tasks(self) -> list[TaskSCHEMA]:
        #Шаг 1: проверка на данные в Redis
        cached_tasks = self.cache.get(self.cache_tasks_key)
        if cached_tasks is not None:
            return cached_tasks

        tasks_orm = self.task_repo.get_all() # Шаг 2: идем в БД если данных нет в Redis
        
        # Шаг 3: Сохранить данные в кэш, если их нет
        task_read = [TaskSCHEMA.model_validate(task) for task in tasks_orm]
        tasks_for_cache = [task.model_dump() for task in task_read]
        self.cache.set(self.cache_tasks_key, tasks_for_cache)

        return task_read #Шаг 4: Ответ


    def create_task(self, create_task: CreateTaskSCHEMA) -> TaskSCHEMA:
        # Инвалидация кэша
        self.cache.delete(self.cache_tasks_key)

        task = self.task_repo.create(title=create_task.title)
        self.db.commit()
        return TaskSCHEMA.model_validate(task)
    

    def update_task(self, task_id: str, update_task: UpdateTaskSCHEMA) -> TaskSCHEMA:
        # Инвалидация кэша
        self.cache.delete(self.cache_tasks_key)

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
        # Инвалидация кэша
        self.cache.delete(self.cache_tasks_key)

        task_for_delete = self.task_repo.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        self.task_repo.delete(task_for_delete)
        self.db.commit()


