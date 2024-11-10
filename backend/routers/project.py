from fastapi import APIRouter, Depends, HTTPException, status

from dao.user import find_user_by_id
from schemas.project import Project, ProjectCreate, Procurement, Stage, Risk, ProcurementResponse, RiskResponse, \
    StageResponse
from schemas.user import UserDao, ContactCreate, Contact, ContactResponse
from utils.token import get_current_user
from dao.project import get_project_by_id, create_project, get_project_by_name, get_projects_by_user, \
    add_contact_to_project, add_procurement_to_project, add_stage_to_project, add_risk_to_project, \
    get_contacts_by_project_id, get_procurements_by_project_id, get_risks_by_project_id, get_stages_by_project_id, \
    get_procurement_by_id

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


@router.get("/{project_id}/get_contacts", response_model=dict[str, list[ContactResponse] | list[None]])
async def get_contacts(project_id: str, user: UserDao = Depends(get_current_user)):
    contacts = await get_contacts_by_project_id(project_id)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"contacts": contacts}


@router.post("/{project_id}/add_procurement", response_model=dict[str, Project | None])
async def add_procurement(project_id: str, procurement_data: Procurement, user: UserDao = Depends(get_current_user)):
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


@router.get("/{project_id}/get_procurement/{procurement_id}", response_model=dict[str, Procurement])
async def get_procurement(project_id: str, procurement_id: str, user: UserDao = Depends(get_current_user)):
    procurement = await get_procurement_by_id(project_id, procurement_id)
    if procurement is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закупка не найдена'
        )
    return {"updated_procurement": procurement}


@router.post("/{project_id}/add_stage", response_model=dict[str, Project | None])
async def add_stage(project_id: str, stage_data: Stage, user: UserDao = Depends(get_current_user)):
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


@router.post("/{project_id}/add_risk", response_model=dict[str, Project | None])
async def add_stage(project_id: str, risk_data: Risk, user: UserDao = Depends(get_current_user)):
    project = await add_risk_to_project(project_id, risk_data)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"updated_project": project}


@router.get("/{project_id}/get_risks", response_model=dict[str, list[RiskResponse] | list[None]])
async def get_risks(project_id: str, user: UserDao = Depends(get_current_user)):
    risks = await get_risks_by_project_id(project_id)
    if risks is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"risks": risks}
