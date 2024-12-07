from fastapi import APIRouter, Depends, HTTPException, status

from dao.user import UserDao
from schemas.user import User, UserCreateSchema, UserResponse, Role
from utils.password import get_password_hash
from utils.role import get_admin_role, get_foreman_role
from utils.token import get_current_user

router = APIRouter()


@router.post("/register")
async def register_user(user_data: UserCreateSchema, admin: User = Depends(get_admin_role)) -> dict:
    user = await UserDao.find_user_by_email(user_data.email.lower())
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )

    user_data.password = get_password_hash(user_data.password)
    user_id = await UserDao.create_user(user_data)
    return {"status": "success", "user_id": user_id}


@router.get("/get")
async def get_users() -> dict[str, list[UserResponse]]:
    users = await UserDao.find_all_users()
    return {"users": users}


@router.get("/find/", response_model=list[UserResponse | None])
async def find_users_by_filters(name: str = "", lastname: str = "", middlename: str = "", role: Role = None,
                                user: User = Depends(get_foreman_role)) -> list[UserResponse | None]:
    users = await UserDao.find_users(name, lastname, middlename, role)
    return users


@router.get("/get_user/{user_id}", response_model=User)
async def get_user(user_id: str, ser: User = Depends(get_current_user)):
    finded_user = await UserDao.find_user_by_id(user_id)
    if finded_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    del finded_user.password
    return finded_user


@router.put("/update/{user_id}", response_model=User)
async def update_user(user_id: str, updated_data: UserCreateSchema, admin: User = Depends(get_admin_role)):
    updated_user = await UserDao.update_user(user_id, updated_data)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    del updated_user.password
    return updated_user
