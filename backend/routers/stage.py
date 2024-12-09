from fastapi import APIRouter, Depends, HTTPException, status

from dao.project import ProjectDao 
from schemas.project import ProjectResponse, Stage, StageResponse, StageUpdate
from schemas.user import User
from utils.role import get_foreman_role
from utils.token import get_current_user

router = APIRouter()


@router.post("/{project_id}/add_stage", response_model=dict[str, ProjectResponse | None])
async def add_stage(project_id: str, stage_data: Stage, foreman: User = Depends(get_foreman_role)):
    project = await ProjectDao.add_stage_to_project(project_id, stage_data)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"updated_project": project}


@router.get("/{project_id}/get_stages", response_model=dict[str, list[StageResponse] | list[None]])
async def get_stages(project_id: str, user: User = Depends(get_current_user)):
    stages = await ProjectDao.get_stages_by_project_id(project_id)
    if stages is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"stages": stages}


@router.get("/{project_id}/get_stage/{stage_id}", response_model=dict[str, StageResponse])
async def get_stage(project_id: str, stage_id: str, user: User = Depends(get_current_user)):
    stage = await ProjectDao.get_stage_by_id(project_id, stage_id)
    if stage is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Этап не найден'
        )
    return {"stage": stage}


@router.put("/{project_id}/update_stage/{stage_id}", response_model=dict[str, StageResponse | None])
async def update_stage(project_id: str, stage_id: str, stage_data: StageUpdate,
                       user: User = Depends(get_foreman_role)):
    stage = await ProjectDao.update_stage_by_id(project_id, stage_id, stage_data)
    if stage is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Этап не найден'
        )

    return {"updated_stage": stage}


@router.delete("/{project_id}/delete_stage/{stage_id}", response_model=dict[str, str])
async def remove_stage(project_id: str, stage_id: str, user: User = Depends(get_foreman_role)):
    deleted_id = await ProjectDao.delete_stage(project_id, stage_id)
    if deleted_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Этап не найден'
        )

    return {"deleted_id": deleted_id}
