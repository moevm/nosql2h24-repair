import re

from bson import ObjectId

from database import db
from schemas.user import UserCreateSchema, UserDao, UserBaseSchema, Contact, ContactResponse, Role
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


async def find_users(name: str = "", lastname: str = "", middlename: str = "", role: Role = None) -> list[
    UserBaseSchema | None]:
    users = db.get_collection('user')

    query = {}
    if name:
        query["name"] = {"$regex": f"^{name}", "$options": "i"}
    if lastname:
        query["lastname"] = {"$regex": f"^{lastname}", "$options": "i"}
    if middlename:
        query["middlename"] = {"$regex": f"^{middlename}", "$options": "i"}
    if role:
        query["role"] = str(role.value)

    cursor = users.find(query)
    user_list = []

    for user in await cursor.to_list():
        user = object_id_to_str(user)
        user_list.append(UserBaseSchema(**user))
    return user_list


async def find_users_from_project(project_id: str, name: str = "", lastname: str = "", middlename: str = "",
                                  role: Role = None) -> list[
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
    matched_contacts = []

    # случай, когда нет фильтров ФИО
    if not search_params:
        # но есть фильтр роли
        if role:
            for contact_id, contact in contacts.items():
                contact_role = contact.get("role", None)
                if contact_role == role.value:
                    matched_contacts.append(ContactResponse(id=contact_id, **contact))
            return matched_contacts
        
        # без фильтров - все контакты проекта
        return [ContactResponse(id=contact_id, **contact) for contact_id, contact in contacts.items()]

    # случай, когда есть фильтры ФИО
    search_query = ".*".join(search_params)
    
    for contact_id, contact in contacts.items():
        username = contact.get("username", "")
        contact_role = contact.get("role", None)
        if re.search(search_query, username, re.IGNORECASE):
            # есть фильтр роли
            if role and contact_role != role.value:
                continue
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
