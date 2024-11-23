from fastapi import APIRouter, Depends, HTTPException, status

from dao.project import add_contact_to_project, get_contacts_by_project_id
from dao.user import find_user_by_id
from schemas.projectresponse import ProjectResponse
from schemas.user import UserDao, ContactCreate, ContactResponse
from utils.token import get_current_user

router = APIRouter()


@router.post("/{project_id}/add_contact", response_model=dict[str, ProjectResponse | None])
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
