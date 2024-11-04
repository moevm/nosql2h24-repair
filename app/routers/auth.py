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


# @router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
# async def create_user(payload: schemas.UserCreateSchema):
#     user = User.find_one({"email": payload.email.lower()})
#     if user:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exists')
# 
#     if payload.password != payload.passwordConfirmed:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password does not match')
# 
#     payload.password = password.get_password_hash(payload.password)
#     del payload.passwordConfirmed
#     payload.role = 'user'
#     payload.verified = True
#     payload.email = payload.email.lower()
#     payload.created_at = datetime.now(timezone.utc)
#     payload.updated_at = payload.created_at
#     result = User.insert(payload.model_dump())
#     new_user = user_response_entity(User.find_one({'_id': result.inserted_id}))
#     return {"status": "success", "user": new_user}

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


# @router.post("/login")
# def login(payload: schemas.UserLoginSchema, response: Response, Authorize: AuthJWT = Depends()):
#     db_user = User.find_one({"email": payload.email.lower()})
#     if not db_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid email or password')
#     user = user_entity(db_user)
# 
#     if not verify_password(payload.password, user['password']):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid email or password')
# 
#     access_token = Authorize.create_access_token(subject=str(user['id']),
#                                                  expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
# 
#     refresh_token = Authorize.create_refresh_token(subject=str(user['id']),
#                                                    expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))
# 
#     response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
#                         ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
# 
#     response.set_cookie('refresh_token', refresh_token, REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60,
#                         '/', None, False, True, 'lax')
# 
#     response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60, ACCESS_TOKEN_EXPIRES_IN * 60, '/', None,
#                         False, True, 'lax')
# 
#     return {'status': 'success', 'access_token': access_token}
# 
# 
# @router.get('/refresh')
# def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_refresh_token_required()
# 
#         user_id = Authorize.get_jwt_subject()
#         if not user_id:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail='Could not refresh access token')
# 
#         user = user_entity(User.find_one({'_id': ObjectId(str(user_id))}))
# 
#         if not user:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail='The user belonging to this token no logger exist')
# 
#         access_token = Authorize.create_access_token(subject=str(user['id']),
#                                                      expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
#     except Exception as e:
#         error = e.__class__.__name__
#         if error == 'MissingTokenError':
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                                 detail='Please provide refresh token')
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
# 
#     response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
#                         ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
# 
#     response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60, ACCESS_TOKEN_EXPIRES_IN * 60, '/', None,
#                         False, True, 'lax')
# 
#     return {'access_token': access_token}
# 
# 
# @router.get('/logout', status_code=status.HTTP_200_OK)
# def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
#     Authorize.unset_jwt_cookies()
#     response.set_cookie('logged_in', '', -1)
# 
#     return {'status': 'success'}
