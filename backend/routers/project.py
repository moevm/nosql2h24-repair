from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from dao.user import UserDao
from schemas.project import ProjectResponse, ProjectCreate, ProjectStatus, ProjectUpdate
from schemas.user import User, Role, UserResponse, ContactResponse, UserCreateSchema
from utils.role import get_customer_role, get_foreman_role
from utils.token import get_current_user
from dao.project import ProjectDao

router = APIRouter()


@router.get("/one/{project_id}", response_model=dict[str, ProjectResponse | None])
async def get_project(project_id: str, user: User = Depends(get_current_user)):
    project = await ProjectDao.get_project_by_id(project_id)
    return {"project": project}


@router.put("/update/{project_id}", response_model=dict[str, ProjectResponse | None])
async def update_project(project_id: str, project_data: ProjectUpdate, user: User = Depends(get_current_user)):
    project = await ProjectDao.update_project_by_id(project_id, project_data)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проекта с id {project_id} не существует",
        )
    return {"project": project}


@router.post("/create", response_model=dict[str, ProjectResponse | None])
async def create(project_data: ProjectCreate, customer: User = Depends(get_customer_role)):
    project = await ProjectDao.get_project_by_name(project_data.name)
    if project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Проект уже существует'
        )
    new_project = await ProjectDao.create_project(project_data, customer)
    if new_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ошибка создания проекта'
        )
    return {"new_project": new_project}


@router.delete("/delete/{project_id}", response_model=dict[str, str])
async def remove_project(project_id: str, user: User = Depends(get_foreman_role)):
    deleted_id = await ProjectDao.delete_project(project_id)
    if deleted_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден'
        )
    return {"deleted_id": deleted_id}


@router.get("/all", response_model=list[ProjectResponse])
async def get_all(project_name: str = "", project_status: ProjectStatus = None, 
                  start_date: datetime = None, end_date: datetime = None, 
                  user = Depends(get_current_user)):
    if user.role == Role.admin:
        return await ProjectDao.get_all_projects(project_name, project_status, start_date, end_date)
    return await ProjectDao.get_all_projects(project_name, project_status, start_date, end_date, user.id)


@router.get("/get_users/{project_id}", response_model=list[ContactResponse | None])
async def get_users(project_id: str, name: str = "", lastname: str = "", middlename: str = "",
                    role: Role = None, user: User = Depends(get_foreman_role)):
    users = await UserDao.find_users_from_project(project_id, name, lastname, middlename, role)

    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проекта не существует'
        )

    return users
