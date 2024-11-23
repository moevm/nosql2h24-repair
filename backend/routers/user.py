from fastapi import APIRouter, Depends, HTTPException, status

from dao.user import find_user_by_email, create_user, find_all_users, find_user_by_id
from schemas.user import UserDao, UserCreateSchema, UserBaseSchema
from utils.password import get_password_hash
from utils.role import get_admin_role
from utils.token import get_current_user

router = APIRouter()


@router.post("/register")
async def register_user(user_data: UserCreateSchema, admin: UserDao = Depends(get_admin_role)) -> dict:
    user = await find_user_by_email(user_data.email.lower())
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )

    user_data.password = get_password_hash(user_data.password)
    user_id = await create_user(user_data)
    return {"status": "success", "user_id": user_id}


@router.get("/get")
async def get_users() -> dict[str, list[UserBaseSchema]]:
    users = await find_all_users()
    return {"users": users}


@router.get("/get_user/{user_id}", response_model=UserDao)
async def get_user(user_id: str, ser: UserDao = Depends(get_current_user)):
    finded_user = await find_user_by_id(user_id)
    if finded_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    del finded_user.password
    return finded_user
