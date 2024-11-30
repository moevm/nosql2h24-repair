from fastapi import APIRouter, HTTPException, status, Depends

from dao.project import add_risk_to_project, get_risks_by_project_id, get_risk_by_id, update_risk_by_id, delete_risk
from schemas.project import ProjectResponse, Risk, RiskResponse, RiskUpdate
from schemas.user import User
from utils.role import get_foreman_role
from utils.token import get_current_user

router = APIRouter()


@router.post("/{project_id}/add_risk", response_model=dict[str, ProjectResponse | None])
async def add_stage(project_id: str, risk_data: Risk, foreman: User = Depends(get_foreman_role)):
    project = await add_risk_to_project(project_id, risk_data)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"updated_project": project}


@router.get("/{project_id}/get_risks", response_model=dict[str, list[RiskResponse] | list[None]])
async def get_risks(project_id: str, user: User = Depends(get_current_user)):
    risks = await get_risks_by_project_id(project_id)
    if risks is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"risks": risks}


@router.get("/{project_id}/get_risk/{risk_id}", response_model=dict[str, RiskResponse])
async def get_risk(project_id: str, risk_id: str, user: User = Depends(get_current_user)):
    risk = await get_risk_by_id(project_id, risk_id)
    if risk is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Риск не найден'
        )
    return {"risk": risk}


@router.put("/{project_id}/update_risk/{risk_id}", response_model=dict[str, RiskResponse | None])
async def update_risk(project_id: str, risk_id: str, risk_data: RiskUpdate, user: User = Depends(get_foreman_role)):
    risk = await update_risk_by_id(project_id, risk_id, risk_data)
    if risk is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Риск не найден'
        )

    return {"updated_risk": risk}


@router.delete("/{project_id}/delete_risk/{risk_id}", response_model=dict[str, str])
async def remove_risk(project_id: str, risk_id: str, user: User = Depends(get_foreman_role)):
    deleted_id = await delete_risk(project_id, risk_id)
    if deleted_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Риск не найден'
        )

    return {"deleted_risk": deleted_id}
