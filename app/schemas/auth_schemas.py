from pydantic import BaseModel, EmailStr
from app.schemas.user_schemas import UserPassword, UserBase
from typing import List

class SignInRequest(UserPassword):
    user_identity: str

class SignUpRequest(UserPassword):
    user_email: EmailStr
    user_firstname: str
    user_lastname: str = None
    user_city: str = None
    user_phone: str = None
    user_links: str = None

class UserUpdateRequest(BaseModel):
    user_firstname: str
    user_lastname: str = None
    user_city: str = None
    user_phone: str = None
    user_links: str = None

class UsersListResponse(BaseModel):
    users: List[UserBase]

class UserDetailResponse(BaseModel):
    user: UserBase
