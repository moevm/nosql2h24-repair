from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


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
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    password: str = Field(min_length=8)


class UserDao(UserBaseSchema):
    password: str = Field(min_length=8)
