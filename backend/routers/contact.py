from fastapi import APIRouter, Depends, HTTPException, status

from dao.project import ProjectDao
from dao.user import UserDao
from schemas.project import ProjectResponse
from schemas.user import User, ContactCreate, ContactResponse
from utils.role import get_foreman_role
from utils.token import get_current_user

router = APIRouter()


@router.post("/{project_id}/add_contact", response_model=dict[str, ProjectResponse | None])
async def add_contact(project_id: str, contact_data: ContactCreate, foreman: User = Depends(get_foreman_role)):
    user_to_add = await UserDao.find_user_by_id(contact_data.user_id)
    if not user_to_add:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователя не существует'
        )
    project = await ProjectDao.add_contact_to_project(project_id, user_to_add)
    return {"updated_project": project}


@router.get("/{project_id}/get_contacts", response_model=dict[str, list[ContactResponse] | list[None]])
async def get_contacts(project_id: str, user: User = Depends(get_current_user)):
    contacts = await ProjectDao.get_contacts_by_project_id(project_id)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"contacts": contacts}


@router.delete("/{project_id}/delete_contact/{contact_id}", response_model=dict[str, ProjectResponse | None])
async def delete_contact(project_id:str, contact_id: str, foreman: User = Depends(get_foreman_role)):
    updated_project = await ProjectDao.delete_contact(project_id, contact_id)
    if updated_project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проекта не существует'
        )
    return {"updated_project": updated_project}
