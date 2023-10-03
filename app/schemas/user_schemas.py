from pydantic import BaseModel, EmailStr, Field
from typing import Union
from datetime import datetime

class UserBase(BaseModel):
    user_email: EmailStr
    user_firstname: str
    user_lastname: Union[str, None] = None
    user_city: Union[str, None] = None
    user_phone: Union[str, None] = None
    user_links: Union[str, None] = None
    user_avatar: Union[str, None] = None
    is_superuser: bool = False

class UserPassword(BaseModel):
    hashed_password: str = Field(..., min_length=8)

class User(UserBase, UserPassword):
    user_id: int

class UserInDB(UserBase, UserPassword):
    created_at: datetime
    updated_at: datetime

