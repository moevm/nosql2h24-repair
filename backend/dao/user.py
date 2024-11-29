import re

from bson import ObjectId

from database import db
from schemas.user import UserCreateSchema, UserDao, UserBaseSchema, Contact, ContactResponse
from schemas.utils import object_id_to_str, get_date_now


async def find_user_by_email(email) -> UserDao | None:
    users = db.get_collection('user')
    user = await users.find_one({'email': email})
    if not user:
        return None
    user = object_id_to_str(user)
    return UserDao(**user)


async def find_user_by_id(user_id: str) -> UserDao | None:
    users = db.get_collection('user')
    user = await users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    user = object_id_to_str(user)
    return UserDao(**user)


async def find_users(name: str = "", lastname: str = "", middlename: str = "") -> list[UserBaseSchema | None]:
    users = db.get_collection('user')

    query = {}
    if name:
        query["name"] = {"$regex": f"^{name}", "$options": "i"}  # Начинается с 'name', регистронезависимо
    if lastname:
        query["lastname"] = {"$regex": f"^{lastname}", "$options": "i"}  # Начинается с 'lastname', регистронезависимо
    if middlename:
        query["middlename"] = {"$regex": f"^{middlename}", "$options": "i"}  # Начинается с 'middlename'

    cursor = users.find(query)
    user_list = []

    for user in await cursor.to_list():
        user = object_id_to_str(user)
        user_list.append(UserBaseSchema(**user))
    return user_list


async def find_users_from_project(project_id: str, name: str = "", lastname: str = "", middlename: str = "") -> list[
                                                                                                                    ContactResponse | None] | None:
    project_collection = db.get_collection('project')

    search_params = []

    if lastname:
        search_params.append(lastname)
    if name:
        search_params.append(name)
    if middlename:
        search_params.append(middlename)

    project = await project_collection.find_one({"_id": ObjectId(project_id)})

    if project is None:
        return None

    contacts = project.get("contacts", {})

    if not search_params:
        return [ContactResponse(id=contact_id, **contact) for contact_id, contact in contacts.items()]

    search_query = ".*".join(search_params)

    matched_contacts = []
    for contact_id, contact in contacts.items():
        username = contact.get("username", "")
        if re.search(search_query, username, re.IGNORECASE):  # Сравнение с username
            matched_contacts.append(ContactResponse(id=contact_id, **contact))

    return matched_contacts


async def find_all_users() -> list[UserBaseSchema | None]:
    users_collection = db.get_collection('user')
    users = users_collection.find()
    users_list = []
    for user in await users.to_list():
        user = object_id_to_str(user)
        users_list.append(UserBaseSchema(**user))
    return users_list


async def create_user(user: UserCreateSchema):
    users_collection = db.get_collection('user')
    user_dict = user.model_dump()
    user_dict['created_at'] = get_date_now()
    user_dict['updated_at'] = get_date_now()
    result = await users_collection.insert_one(user_dict)
    return str(result.inserted_id)
