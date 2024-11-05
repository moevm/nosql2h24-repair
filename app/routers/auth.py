from datetime import datetime, timezone, timedelta

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Response, Depends

from app import schemas
from app.config import settings
from app.database import User
from app.schemas.user import UserCreateSchema, UserLoginSchema
from app.serializers.userSerializers import user_response_entity, user_entity, user_list_entity
from app.utils import password
from app.utils.password import verify_password, pwd_context, create_access_token, get_password_hash
from app.utils.token import get_current_user

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
ALGORITHM = settings.JWT_ALGORITHM
SECRET_KEY = settings.JWT_SECRET_KEY


@router.post("/register")
async def register_user(user_data: UserCreateSchema) -> dict:
    user = User.find_one({"email": user_data.email.lower()})
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )

    if user_data.password != user_data.passwordConfirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пароли не совпадают'
        )

    user_data.password = get_password_hash(user_data.password)
    del user_data.passwordConfirmed
    result = User.insert_one(user_data.model_dump())
    new_user = user_response_entity(User.find_one({'_id': result.inserted_id}))
    return {"status": "success", "user": new_user}


@router.get("/get")
async def get_users() -> dict:
    users = User.find({})
    return {"users": user_list_entity(users)}


@router.post("/login")
async def login_user(response: Response, user_data: UserLoginSchema) -> dict:
    user = user_entity(User.find_one({"email": user_data.email.lower()}))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователя не существует'
        )
    if not verify_password(user_data.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный пароль'
        )
    access_token = create_access_token({"sub": user['id']})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
