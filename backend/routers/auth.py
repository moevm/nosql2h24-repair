from typing import List
from fastapi import APIRouter, HTTPException, status, Response, Depends

from config import settings
from dao.user import find_all_users, find_user_by_email, create_user, find_user_by_id
from schemas.user import UserCreateSchema, UserLoginSchema, UserDao, UserBaseSchema
from utils.password import verify_password, create_access_token, get_password_hash
from utils.role import get_admin_role
from utils.token import get_current_user

router = APIRouter()


@router.post("/login")
async def login_user(response: Response, user_data: UserLoginSchema) -> dict:
    user = await find_user_by_email(user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователя не существует'
        )
    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный пароль'
        )
    access_token = create_access_token({"sub": user.id})
    response.set_cookie(
        key="users_access_token",
        value=access_token,
        secure=False,
        httponly=True,
        samesite='lax')
    return {'access_token': access_token, 'refresh_token': None}


@router.get("/me/")
async def get_me(user_data: UserDao = Depends(get_current_user)):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
