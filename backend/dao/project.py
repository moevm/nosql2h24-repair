from bson import ObjectId
from datetime import datetime, timezone
from database import db
from schemas.project import ProjectCreate, Project, ProjectResponse
from schemas.user import UserCreateSchema, UserDao, UserBaseSchema, Contact
from schemas.utils import object_id_to_str


async def create_project(project_crate: ProjectCreate, user: UserDao) -> ProjectResponse:
    project_collection = db.get_collection('project')
    project = Project(**project_crate.model_dump())
    contact = Contact(
        username=f'{user.lastname} {user.name} {user.middlename}',
        role=user.role
    )
    project.add_contact(user.id, contact)
    result = await project_collection.insert_one(project.model_dump())
    return await get_project_by_id(result.inserted_id)


async def get_project_by_id(project_id: str) -> ProjectResponse | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({'_id': ObjectId(project_id)})
    if project is None:
        return None
    project = object_id_to_str(project)
    return ProjectResponse(**project)


async def get_project_by_name(project_name: str) -> ProjectResponse | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({'name': project_name})
    if project is None:
        return None
    project = object_id_to_str(project)
    return ProjectResponse(**project)


async def get_projects_by_user(user_id: str) -> list[ProjectResponse] | None:
    project_collection = db.get_collection('project')
    cursor = project_collection.find(
        {f"contacts.{user_id}": {"$exists": True}}
    )
    projects_list = await cursor.to_list()
    result = []
    for project in projects_list:
        project = object_id_to_str(project)
        result.append(ProjectResponse(**project))
    return result
