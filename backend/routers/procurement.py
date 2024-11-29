from fastapi import APIRouter, Depends, HTTPException, status

from dao.project import add_procurement_to_project, get_procurements_by_project_id, get_procurement_by_id, \
    update_procurement_by_id, delete_procurement
from schemas.project import ProjectResponse, Procurement, ProcurementResponse, ProcurementUpdate
from schemas.user import Contact, UserDao
from utils.role import get_foreman_role
from utils.token import get_current_user

router = APIRouter()


@router.post("/{project_id}/add_procurement", response_model=dict[str, ProjectResponse | None])
async def add_procurement(project_id: str, procurement_data: Procurement, foreman: UserDao = Depends(get_foreman_role)):
    procurement_data.created_by = Contact(
        username=f'{foreman.lastname} {foreman.name} {foreman.middlename}',
        role=foreman.role
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


@router.put("/{project_id}/update_procurement/{procurement_id}", response_model=dict[str, ProcurementResponse | None])
async def update_procurement(project_id: str, procurement_id: str, procurement_data: ProcurementUpdate,
                             user: UserDao = Depends(get_foreman_role)):
    procurement_data.created_by = Contact(
        username=f'{user.lastname} {user.name} {user.middlename}',
        role=user.role
    )

    procurement = await update_procurement_by_id(project_id, procurement_id, procurement_data)
    if procurement is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закупка не найдена'
        )

    return {"updated_procurement": procurement}


@router.delete("/{project_id}/delete_procurement/{procurement_id}", response_model=dict[str, str])
async def remove_procurement(project_id: str, procurement_id: str, user: UserDao = Depends(get_foreman_role)):
    deleted_id = await delete_procurement(project_id, procurement_id)
    if deleted_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закупка не найдена'
        )

    return {"deleted_id": deleted_id}
