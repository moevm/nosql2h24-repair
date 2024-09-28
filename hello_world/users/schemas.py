from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=32)
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    middle_name: str = Field(min_length=3, max_length=50)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=32)
