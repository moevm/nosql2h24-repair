from fastapi import APIRouter, Depends, HTTPException, status

from dao.user import find_user_by_id
from schemas.project import Project, ProjectCreate, Procurement
from schemas.user import UserDao, ContactCreate
from utils.token import get_current_user
from dao.project import get_project_by_id, create_project, get_project_by_name, get_projects_by_user, \
    add_contact_to_project, add_procurement_to_project

router = APIRouter()


@router.get("/one/{project_id}", response_model=dict[str, Project | None])
async def get_project(project_id: str, user: UserDao = Depends(get_current_user)):
    project = await get_project_by_id(project_id)
    return {"project": project}


@router.post("/create", response_model=dict[str, Project | None])
async def create(project_data: ProjectCreate, user: UserDao = Depends(get_current_user)):
    project = await get_project_by_name(project_data.name)
    if project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Проект уже существует'
        )
    new_project = await create_project(project_data, user)
    return {"new_project": new_project}

@router.get("/all", response_model=list[Project])
async def get_all(user: UserDao = Depends(get_current_user)):
    return await get_projects_by_user(user.id)


@router.post("/{project_id}/add_contact", response_model=dict[str, Project | None])
async def add_contact(project_id: str, contact_data: ContactCreate, user: UserDao = Depends(get_current_user)):
    user_to_add = await find_user_by_id(contact_data.user_id)
    if not user_to_add:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователя не существует'
        )
    project = await add_contact_to_project(project_id, user_to_add)
    return {"updated_project": project}


@router.post("/{project_id}/add_procurement", response_model=dict[str, Project | None])
async def add_procurement(project_id: str, procurement_data: Procurement, user: UserDao = Depends(get_current_user)):
    project = await add_procurement_to_project(project_id, procurement_data)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"updated_project": project}