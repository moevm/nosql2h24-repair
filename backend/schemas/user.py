from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, root_validator, model_validator, field_serializer


class Role(str, Enum):
    admin = "Администратор"
    foreman = "Прораб"
    worker = "Рабочий"
    customer = "Заказчик"


class UserCreateSchema(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    lastname: str = Field(..., min_length=1, max_length=100, description="Фамилия пользователя")
    middlename: Optional[str] = Field(None, max_length=100, description="Отчество пользователя")
    password: str = Field(min_length=8)
    role: Role

    class Config:
        from_attributes = True


class UserBaseSchema(UserCreateSchema):
    id: str
    created_at: datetime | None = datetime.now(timezone.utc)
    updated_at: datetime | None = datetime.now(timezone.utc)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    password: str = Field(min_length=8)


class UserDao(UserBaseSchema):
    password: str = Field(min_length=8)


class Contact(BaseModel):
    username: str
    role: Role = Role.worker
    created_at: datetime | None = datetime.now(timezone.utc)
    updated_at: datetime | None = datetime.now(timezone.utc)


class ContactCreate(BaseModel):
    user_id: str


class Worker(BaseModel):
    id: str
    name: str
