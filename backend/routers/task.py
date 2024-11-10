import asyncio

from fastapi import APIRouter, Depends, HTTPException, status

from dao.project import get_contacts_by_project_id
from dao.task import add_task, get_all_tasks_by_user, get_task_by_id, add_worker_to_task
from dao.user import find_user_by_id
from schemas.task import Task, TaskResponse
from schemas.user import UserDao, Role, Worker
from utils.token import get_current_user

router = APIRouter()


@router.post('/create/{project_id}/{stage_id}', response_model=TaskResponse)
async def create_task(project_id: str, stage_id: str, task_data: Task, user: UserDao = Depends(get_current_user)):
    if user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав'
        )
    new_task = await add_task(project_id, stage_id, task_data)
    if new_task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Ошибка добавления в проект'
        )
    return new_task


@router.get('/{project_id}/{stage_id}/{task_id}', response_model=TaskResponse)
async def get_task(project_id: str, stage_id: str, task_id: str, user: UserDao = Depends(get_current_user)):
    task = await get_task_by_id(project_id, stage_id, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )
    return task


@router.get('/get_all', response_model=list[TaskResponse] | list[None])
async def get_all_tasks(user: UserDao = Depends(get_current_user)):
    tasks = await get_all_tasks_by_user(user.id)
    return tasks


@router.put('/{project_id}/{stage_id}/{task_id}/{worker_id}', response_model=TaskResponse)
async def add_worker(project_id: str, stage_id: str, task_id: str, worker_id: str,
                     user: UserDao = Depends(get_current_user)):
    contacts = await get_contacts_by_project_id(project_id)
    for contact in contacts:
        if contact.id == worker_id:
            worker = Worker(
                name=contact.username,
                role=contact.role
            )
            result = await add_worker_to_task(project_id, stage_id, task_id, worker_id, worker)
            if result:
                return result
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Задача или этап не найдены'
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Работник отсутствует в контактах проекта'
    )
