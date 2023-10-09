from pydantic import BaseModel, EmailStr, Field, validator
from typing import Union, Optional, List, Dict
from datetime import datetime
from enum import Enum as PydanticEnum


class UserStatusEnum(str, PydanticEnum):
    active = 'active'
    inactive = 'inactive'


class UserPassword(BaseModel):
    hashed_password: str = Field(..., min_length=8)

class User(UserPassword):
    id: int
    user_email: EmailStr
    user_firstname: str
    user_lastname: Union[str, None] = None
    user_status: UserStatusEnum = UserStatusEnum.active
    user_city: Union[str, None] = None
    user_phone: Union[str, None] = None
    user_links: Union[str, None] = None
    user_avatar: Union[str, None] = None
    is_superuser: Union[bool, None] = False
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None

class UserGet(BaseModel):
    id: int
    user_email: EmailStr
    user_firstname: str

class UserUpdate(BaseModel):
    user_firstname: str
    user_email: EmailStr
    user_lastname: Union[str, None] = None
    user_city: Union[str, None] = None
    user_phone: Union[str, None] = None
    user_links: Union[str, None] = None
    user_avatar: Union[str, None] = None

    @validator('user_email', pre=True, always=True)
    def prevent_email_change(cls, v, values):
        if 'user_email' in values:
            return values['user_email']
        return v

class UserSignIn(UserPassword):
    user_email: EmailStr
    user_firstname: str

class UsersListResponse(BaseModel):
    users: List[UserGet]
    
class ErrorResponse(BaseModel):
    detail: str