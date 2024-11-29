from fastapi import APIRouter, Depends, HTTPException, status

from dao.user import find_users_from_project
from schemas.project import ProjectResponse, ProjectCreate, ProjectUpdate
from schemas.user import UserDao, Role, UserBaseSchema, ContactResponse
from utils.role import get_customer_role, get_foreman_role
from utils.token import get_current_user
from dao.project import get_project_by_id, create_project, get_project_by_name, get_projects_by_user, get_all_projects, \
    update_project_by_id

router = APIRouter()


@router.get("/one/{project_id}", response_model=dict[str, ProjectResponse | None])
async def get_project(project_id: str, user: UserDao = Depends(get_current_user)):
    project = await get_project_by_id(project_id)
    return {"project": project}


@router.put("/update/{project_id}", response_model=dict[str, ProjectResponse | None])
async def update_project(project_id: str, project_data: ProjectUpdate, user: UserDao = Depends(get_current_user)):
    project = await update_project_by_id(project_id, project_data)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проекта с id {project_id} не существует",
        )
    return {"project": project}


@router.post("/create", response_model=dict[str, ProjectResponse | None])
async def create(project_data: ProjectCreate, customer: UserDao = Depends(get_customer_role)):
    project = await get_project_by_name(project_data.name)
    if project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Проект уже существует'
        )
    new_project = await create_project(project_data, customer)
    return {"new_project": new_project}


@router.get("/all", response_model=list[ProjectResponse])
async def get_all(user: UserDao = Depends(get_current_user)):
    if user.role == Role.admin:
        return await get_all_projects()
    return await get_projects_by_user(user.id)


@router.get("/get_users/{project_id}", response_model=list[ContactResponse | None])
async def get_users(project_id: str, name: str = "", lastname: str = "", middlename: str = "",
                    user: UserDao = Depends(get_foreman_role)):
    users = await find_users_from_project(project_id, name, lastname, middlename)
    
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проекта не существует'
        )

    return users
