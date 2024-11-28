from fastapi import APIRouter, Depends, HTTPException, status

from dao.project import add_stage_to_project, get_stages_by_project_id, get_stage_by_id
from schemas.project import ProjectResponse, Stage, StageResponse
from schemas.user import UserDao
from utils.role import get_foreman_role
from utils.token import get_current_user

router = APIRouter()


@router.post("/{project_id}/add_stage", response_model=dict[str, ProjectResponse | None])
async def add_stage(project_id: str, stage_data: Stage, foreman: UserDao = Depends(get_foreman_role)):
    project = await add_stage_to_project(project_id, stage_data)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"updated_project": project}


@router.get("/{project_id}/get_stages", response_model=dict[str, list[StageResponse] | list[None]])
async def get_stages(project_id: str, user: UserDao = Depends(get_current_user)):
    stages = await get_stages_by_project_id(project_id)
    if stages is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"stages": stages}


@router.get("/{project_id}/get_stage/{stage_id}", response_model=dict[str, StageResponse])
async def get_stage(project_id: str, stage_id: str, user: UserDao = Depends(get_current_user)):
    stage = await get_stage_by_id(project_id, stage_id)
    if stage is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Этап не найден'
        )
    return {"stage": stage}
