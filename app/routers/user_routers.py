import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Any
from datetime import timedelta

from app.db.database import get_db
from app.models.models import UserModel
from app.schemas.user_schemas import UserGet, UserSignIn, UserUpdate, ErrorResponse
from app.services.crud_user import UserCRUD


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

user_endpoints = APIRouter()
crud = UserCRUD(UserModel)


@user_endpoints.get("/users/", response_model=List[UserGet])
async def get_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    try:
        query = await crud.get_multi(db, skip=skip, limit=limit)
        return query.scalars()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)

@user_endpoints.get("/user/{id}", response_model=Union[UserGet, ErrorResponse])
async def get_user_by_id(id: int, db: AsyncSession = Depends(get_db)):
    try:
        user: UserModel = await crud.get(db=db, id=id)
        return crud.check_user(user)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)

@user_endpoints.post("/user/")
async def create_user(user_data: UserSignIn, db: AsyncSession = Depends(get_db)):
    try:
        return    await crud.create(db=db, user_data=user_data)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)

@user_endpoints.put("/user/{id}", response_model=Union[UserUpdate, ErrorResponse])
async def update_user(id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.update(db, id, user_data)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)

@user_endpoints.patch("/user/{id}")
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.delete(db, id)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)
