import logging
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from datetime import timedelta
from jose import jwt
from pydantic import ValidationError

from app.db.database import get_db
from app.models.models import UserModel
from app.schemas.user_schemas import UserGet
from app.schemas.token import Token, TokenPayload
from app.services.crud_user import UserCRUD
from app.services.hashing import PasswordContext
from app.config.app_config import server_setting
from app.utils.auth0 import VerifyToken

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/signin"
)
token_auth_scheme = HTTPBearer()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

router = APIRouter()
crud = UserCRUD(UserModel)

@router.get('/api/private')
async def private(response: Response, token: str = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()
    if result.get('status'):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    return result


@router.post('/signin', response_model=Token)
async def signin(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    try:
        user = await crud.authenticate(db, email=form_data.username, password=form_data.password)
        access_token_expires = timedelta(minutes=PasswordContext.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": PasswordContext.create_access_token(
                user.user_email, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)

@router.get('/me', response_model=UserGet)
async def jwt_get_user(token: str = Depends(token_auth_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = VerifyToken(token.credentials).verify()
        print(payload)
        user = await crud.get_by_email(db, email=payload['email'])
        user = user.scalar()
        return crud.check_user(user)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)    
