from bson import ObjectId
from pydantic import BaseModel

from database import User
from schemas.user import UserResponseSchema, UserCreateSchema, UserDao


def object_id_to_str(user) -> dict[str, str]:
    user['id'] = str(user['_id'])
    return user


def find_user_by_email(email) -> UserDao | None:
    user = User.find_one({'email': email})
    if not user:
        return None
    user = object_id_to_str(user)
    return UserDao(**user)


def find_user_by_id(user_id: ObjectId) -> UserDao | None:
    user = User.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    user = object_id_to_str(user)
    return UserDao(**user)


def find_all_users() -> list[UserResponseSchema]:
    users = User.find({})
    users_list = []
    for user in users:
        user = object_id_to_str(user)
        users_list.append(UserResponseSchema(**user))
    return users_list


def create_user(user: UserCreateSchema):
    result = User.insert_one(user.model_dump())
    return str(result.inserted_id)
