from fastapi import APIRouter, Depends, HTTPException, status

from dao.project import add_procurement_to_project, get_procurements_by_project_id, get_procurement_by_id
from schemas.projectresponse import ProjectResponse, Procurement, ProcurementResponse
from schemas.user import Contact, UserDao
from utils.token import get_current_user

router = APIRouter()


@router.post("/{project_id}/add_procurement", response_model=dict[str, ProjectResponse | None])
async def add_procurement(project_id: str, procurement_data: Procurement, user: UserDao = Depends(get_current_user)):
    procurement_data.created_by = Contact(
        username=f'{user.lastname} {user.name} {user.middlename}',
        role=user.role
    )
    project = await add_procurement_to_project(project_id, procurement_data)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"updated_project": project}


@router.get("/{project_id}/get_procurements", response_model=dict[str, list[ProcurementResponse] | list[None]])
async def get_procurements(project_id: str, user: UserDao = Depends(get_current_user)):
    procurements = await get_procurements_by_project_id(project_id)
    if procurements is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"procurements": procurements}


@router.get("/{project_id}/get_procurement/{procurement_id}", response_model=dict[str, ProcurementResponse])
async def get_procurement(project_id: str, procurement_id: str, user: UserDao = Depends(get_current_user)):
    procurement = await get_procurement_by_id(project_id, procurement_id)
    if procurement is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закупка не найдена'
        )
    return {"procurement": procurement}
