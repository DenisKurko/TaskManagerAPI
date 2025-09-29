from db.schemas.tasks import TaskCreateSchema, TaskSchema
from utils.repository import AbstractRepo


class TasksService:
    def __init__(self, tasks_repo: AbstractRepo) -> None:
        self.tasks_repo = tasks_repo() # type: ignore
        
    
    async def add(self, task: TaskCreateSchema):
        task_dict = task.model_dump()
        task_id = await self.tasks_repo.add(task_dict)
        
        return task_id
    
    
    async def find_all(self, **filter_by) -> list[TaskSchema]:
        tasks = await self.tasks_repo.find_all(**filter_by)
        
        return tasks
    
    
    async def find(self, **filter_by) -> TaskSchema:
        task = await self.tasks_repo.find(**filter_by)
        
        return task
    
    
    async def delete(self, **filter_by) -> TaskSchema:
        task = await self.tasks_repo.delete(**filter_by)
        
        return task