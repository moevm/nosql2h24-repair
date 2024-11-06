from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr
    role: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class UserCreateSchema(UserBaseSchema):
    password: str = Field(min_length=8)
    passwordConfirmed: str = Field(min_length=8)
    verified: bool = False


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponseSchema(UserBaseSchema):
    id: str 

class UserDao(UserResponseSchema):
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema
