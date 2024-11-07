from bson import ObjectId
from datetime import datetime, timezone
from database import db
from schemas.user import UserCreateSchema, UserDao, UserBaseSchema


def object_id_to_str(user) -> dict[str, str]:
    user['id'] = str(user['_id'])
    return user


async def find_user_by_email(email) -> UserDao | None:
    users = db.get_collection('user')
    user = await users.find_one({'email': email})
    if not user:
        return None
    user = object_id_to_str(user)
    return UserDao(**user)


async def find_user_by_id(user_id: ObjectId) -> UserDao | None:
    users = db.get_collection('user')
    user = await users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    user = object_id_to_str(user)
    return UserDao(**user)


async def find_all_users() -> list[UserBaseSchema]:
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
    user_dict['created_at'] = datetime.now(timezone.utc)
    user_dict['updated_at'] = datetime.now(timezone.utc)
    result = await users_collection.insert_one(user_dict)
    return str(result.inserted_id)
