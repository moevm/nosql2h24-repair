from bson import ObjectId
from datetime import datetime, timezone
from database import db
from schemas.project import ProjectCreate, Project, Procurement, Procurement
from schemas.user import UserCreateSchema, UserDao, UserBaseSchema, Contact
from schemas.utils import object_id_to_str, generate_id


async def create_project(project_crate: ProjectCreate, user: UserDao) -> Project:
    project_collection = db.get_collection('project')
    contact = Contact(
        username=f'{user.lastname} {user.name} {user.middlename}',
        role=user.role
    )
    project_crate.add_contact(user.id, contact)
    result = await project_collection.insert_one(project_crate.model_dump())
    return await get_project_by_id(result.inserted_id)


async def get_project_by_id(project_id: str) -> Project | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({'_id': ObjectId(project_id)})
    if project is None:
        return None
    project = object_id_to_str(project)
    return Project(**project)


async def get_project_by_name(project_name: str) -> Project | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({'name': project_name})
    if project is None:
        return None
    project = object_id_to_str(project)
    return Project(**project)


async def get_projects_by_user(user_id: str) -> list[Project] | None:
    project_collection = db.get_collection('project')
    cursor = project_collection.find(
        {f"contacts.{user_id}": {"$exists": True}}
    )
    projects_list = await cursor.to_list()
    result = []
    for project in projects_list:
        project = object_id_to_str(project)
        result.append(Project(**project))
    return result


async def add_contact_to_project(project_id: str, user: UserDao) -> Project | None:
    project_collection = db.get_collection('project')
    result = await project_collection.update_one(
        {"_id": ObjectId(project_id)},
        {
            "$set": {
                f"contacts.{user.id}": {
                    "username": f"{user.lastname} {user.name} {user.middlename}",
                    "role": user.role,
                }
            }
        },
    )
    return await get_project_by_id(project_id)


async def add_procurement_to_project(project_id: str, procurement_create: Procurement) -> Project | None:
    project_collection = db.get_collection('project')
    procurement = procurement_create.model_dump()
    procurement['quantity'] = str(procurement['quantity'])
    procurement['price'] = str(procurement['price'])
    result = await project_collection.update_one(
        {"_id": ObjectId(project_id)},
        {
            "$set": {f"procurements.{generate_id()}": procurement}
        }
    )
    return await get_project_by_id(project_id)
