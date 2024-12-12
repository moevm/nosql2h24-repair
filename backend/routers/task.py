from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from dao.project import ProjectDao
from dao.task import TaskDAO
from schemas.task import Task, TaskResponse, TaskStatus, TaskUpdate, ProjectTaskResponse, TaskStatusUpdate
from schemas.user import User, Worker
from utils.role import get_foreman_role
from utils.token import get_current_user

router = APIRouter()


@router.post('/create/{project_id}/{stage_id}', response_model=TaskResponse)
async def create_task(project_id: str, stage_id: str, task_data: Task, foreman: User = Depends(get_foreman_role)):
    new_task = await TaskDAO.add_task(project_id, stage_id, task_data)
    if new_task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Ошибка добавления задачи в проект'
        )
    return new_task


@router.get('/get_task/{project_id}/{stage_id}/{task_id}', response_model=TaskResponse)
async def get_task(project_id: str, stage_id: str, task_id: str, user: User = Depends(get_current_user)):
    task = await TaskDAO.get_task_by_id(project_id, stage_id, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )
    return task


@router.delete('/delete/{project_id}/{stage_id}/{task_id}')
async def remove_task(project_id: str, stage_id: str, task_id: str, user: User = Depends(get_foreman_role)):
    deleted_id = await TaskDAO.remove_task(project_id, stage_id, task_id)
    if deleted_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )
    return deleted_id


@router.put('/update_task/{project_id}/{stage_id}/{task_id}', response_model=TaskResponse)
async def update_task(project_id: str, stage_id: str, task_id: str, task_data: TaskUpdate,
                      user: User = Depends(get_foreman_role)):
    task = await TaskDAO.update_task_by_id(project_id, stage_id, task_id, task_data)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )
    return task

@router.put('/update_status_task/{project_id}/{stage_id}/{task_id}', response_model=TaskResponse)
async def update_status_task(project_id: str, stage_id: str, task_id: str, task_data: TaskStatusUpdate,
                             user: User = Depends(get_current_user)):
    updated_task = await TaskDAO.update_task_status(project_id, stage_id, task_id, task_data)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача не найдена'
        )
    return updated_task


@router.get('/get_stage_tasks/{project_id}/{stage_id}', response_model=list[TaskResponse] | list[None])
async def get_stage_tasks(project_id: str, stage_id: str):
    tasks = await TaskDAO.get_tasks_by_stage_id(project_id, stage_id)
    return tasks


@router.get('/get_all', response_model=list[ProjectTaskResponse] | list[None])
async def get_all_tasks(task_name: str = "", project_name: str = "", task_status: TaskStatus = TaskStatus.none_status, 
                        start_date: datetime = None, end_date: datetime = None, 
                        user: User = Depends(get_current_user)):
    tasks = await TaskDAO.get_all_tasks_by_user(user.id, task_name, project_name, task_status)
    return tasks


@router.put('/{project_id}/{stage_id}/{task_id}/{worker_id}', response_model=TaskResponse)
async def add_worker(project_id: str, stage_id: str, task_id: str, worker_id: str,
                     foreman: User = Depends(get_foreman_role)):
    contacts = await ProjectDao.get_contacts_by_project_id(project_id)
    for contact in contacts:
        if contact.id == worker_id:
            worker = Worker(
                name=contact.username,
                role=contact.role
            )
            result = await TaskDAO.add_worker_to_task(project_id, stage_id, task_id, worker_id, worker)
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


@router.delete('/{project_id}/{stage_id}/{task_id}/{worker_id}', response_model=dict[str, str])
async def delete_worker(project_id: str, stage_id: str, task_id: str, worker_id: str,
                        foreman: User = Depends(get_foreman_role)):
    delete_id = await TaskDAO.delete_worker_from_task(project_id, stage_id, task_id, worker_id)

    if delete_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Работник не привязан к задаче'
        )

    return {"delete_id": delete_id}
