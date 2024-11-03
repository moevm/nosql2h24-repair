from datetime import datetime
from pydantic import BaseModel, constr, EmailStr


class UserBaseSchema(BaseModel):
    name: str
    email: str
    role: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        orm_mode = True
    
    
class UserCreateSchema(UserBaseSchema):
    password: constr(min_length=8, max_length=128)
    passwordConfirmed: constr(min_length=8, max_length=128)
    verified: bool = False
    
    
class UserLoginSchema(UserBaseSchema):
    email: EmailStr
    password: constr(min_length=8, max_length=128)
    
class UserResponseSchema(UserBaseSchema):
    id: str
    
class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema
