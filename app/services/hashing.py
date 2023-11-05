from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Union, Any
from app.config.app_config import server_setting


class HashContext:
    SCHEMES = ['bcrypt']

    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return CryptContext(schemes=PasswordContext.SCHEMES).verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return CryptContext(schemes=PasswordContext.SCHEMES).hash(password)


class JWTContext:
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 20
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


    @staticmethod
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
        if isinstance(data, dict):
            to_encode = data.copy()
        else:
            to_encode = {"email": str(data)}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=PasswordContext.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, server_setting.JWT_SECRET_KEY, algorithm=PasswordContext.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=PasswordContext.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, server_setting.JWT_REFRESH_SECRET_KEY, algorithm=PasswordContext.ALGORITHM)
        return encoded_jwt

class PasswordContext(HashContext, JWTContext):
    pass





    


