from fastapi import APIRouter, Request, Depends

from db.schemas.tasks import TaskCreateSchema, TaskPostSchema, TaskSchema
from services.tasks import TasksService

from api.dependencies import tasks_service

from typing import Annotated


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("")
async def add_task(
    request: Request,
    task: TaskPostSchema,
    tasks_service: Annotated[TasksService, Depends(tasks_service)],
):
    user_id = request.state.user.get("user_id")
    
    db_task = TaskCreateSchema(
        author_id=user_id,
        title=task.title,
        description=task.description,
        status=task.status
    )
    
    task_id = await tasks_service.add(db_task)
        
    return {
        "task_id": task_id
    }


@router.get("")
async def get_tasks(
    request: Request,
    tasks_service: Annotated[TasksService, Depends(tasks_service)]
) -> list[TaskSchema]:
    user_id = request.state.user.get("user_id")
    
    tasks = await tasks_service.find_all(author_id = user_id)
    
    return tasks


@router.get("/{task_id}")
async def get_task(
    request: Request,
    task_id: int,
    tasks_service: Annotated[TasksService, Depends(tasks_service)]
) -> TaskSchema:
    user_id = request.state.user.get("user_id")
    
    task = await tasks_service.find(author_id = user_id, id = task_id)
    
    return task


@router.delete("/{task_id}")
async def delete_task(
    request: Request,
    task_id: int,
    task_service: Annotated[TasksService, Depends(tasks_service)]
):
    user_id = request.state.user.get("user_id")
    
    deleted_id = await task_service.delete(author_id = user_id, id = task_id)
    
    return {"task_id": deleted_id}