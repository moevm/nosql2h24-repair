import re
from bson import ObjectId

from dao.base import BaseDao
from database import db
from schemas.user import UserCreateSchema, User, UserResponse, Contact, ContactResponse, Role
from schemas.utils import object_id_to_str, get_date_now
from utils.password import get_password_hash


class UserDao(BaseDao):
    collection = db.get_collection('user')

    @classmethod
    async def find_user_by_email(cls, email) -> User | None:
        user = await cls._get_one_by_field('email', email)
        if not user:
            return None
        return User(**user)

    @classmethod
    async def find_user_by_id(cls, user_id: str) -> User | None:
        user = await cls._get_one_by_id(user_id)
        if not user:
            return None
        return User(**user)

    @classmethod
    async def find_users(cls, name: str = "", lastname: str = "", middlename: str = "", role: Role = None) -> list[
        UserResponse | None]:

        query = {}
        if name:
            query["name"] = {"$regex": f"^{name}", "$options": "i"}
        if lastname:
            query["lastname"] = {"$regex": f"^{lastname}", "$options": "i"}
        if middlename:
            query["middlename"] = {"$regex": f"^{middlename}", "$options": "i"}
        if role:
            query["role"] = str(role.value)

        cursor = cls.collection.find(query)
        user_list = []

        for user in await cursor.to_list():
            user = object_id_to_str(user)
            user_list.append(UserResponse(**user))
        return user_list

    @classmethod
    async def find_users_from_project(cls, project_id: str, name: str = "", lastname: str = "", middlename: str = "",
                                      role: Role = None) -> list[
                                                                ContactResponse | None] | None:
        project_collection = db.get_collection('project')

        search_params = {}

        if lastname:
            search_params["lastname"] = lastname
        if name:
            search_params["name"] = name
        if middlename:
            search_params["middlename"] = middlename

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
            fio = username.split()
            contact_role = contact.get("role", None)

            if "lastname" in search_params and len(fio) > 0:
                lastname_match = re.search(search_params["lastname"], fio[0], re.IGNORECASE)
            else:
                lastname_match = True  # Если lastname не указан, то считаем его найденным

            # Проверяем наличие имени
            if "name" in search_params and len(fio) > 1:
                name_match = re.search(search_params["name"], fio[1], re.IGNORECASE)
            else:
                name_match = True  # Если name не указан, то считаем его найденным

            # Проверяем наличие отчества
            if "middlename" in search_params and len(fio) > 2:
                middlename_match = re.search(search_params["middlename"], fio[2], re.IGNORECASE)
            else:
                middlename_match = True  # Если middlename не указан, то считаем его найденным

            # Условие совпадения всех параметров
            if lastname_match and name_match and middlename_match:
                if role and contact_role != role.value:
                    continue
                matched_contacts.append(ContactResponse(id=contact_id, **contact))

        return matched_contacts

    @classmethod
    async def find_all_users(cls) -> list[UserResponse | None]:
        users = cls.collection.find()
        users_list = []
        for user in await users.to_list():
            user = object_id_to_str(user)
            users_list.append(UserResponse(**user))
        return users_list

    @classmethod
    async def create_user(cls, user: UserCreateSchema):
        user_dict = user.model_dump()
        return await cls._create(user_dict)
    
    @classmethod
    async def update_user(cls, user_id: str, user_update: UserCreateSchema):
        update_data = user_update.model_dump()
        update_data["password"] = get_password_hash(update_data["password"])
        updated_id = await cls._update(user_id, update_data)
        return await cls.find_user_by_id(updated_id)

