from fastapi import APIRouter, Depends, HTTPException, status

from schemas.project import Project, ProjectCreate
from schemas.user import UserDao
from utils.token import get_current_user
from dao.project import get_project_by_id, create_project, get_project_by_name

router = APIRouter()


@router.get("/{project_id}", response_model=dict[str, Project])
async def get_project(project_id: str, user: UserDao = Depends(get_current_user)):
    project = await get_project_by_id(project_id)
    return {"project": project}


@router.post("/create", response_model=dict[str, Project])
async def create(project_data: ProjectCreate, user: UserDao = Depends(get_current_user)):
    project = await get_project_by_name(project_data.name)
    if project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Проект уже существует'
        )
    new_project = await create_project(project_data, user)
    return {"new_project": new_project}
