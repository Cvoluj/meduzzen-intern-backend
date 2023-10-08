import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from typing import List, Union
from pydantic import BaseModel

from app.db.database import get_db
from app.models.models import UserModel
from app.schemas.user_schemas import UserGet, UserSignIn, UserUpdate, ErrorResponse, UsersListResponse
from app.services.hashing import PasswordContext
from app.services.crud_base import CRUDBaseGet


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

user_endpoints = APIRouter()

class UserCRUD(CRUDBaseGet):

    def check_user(self, user: UserModel):
        if not user or user.user_status == 'inactive':
            logger.error("User not found")
            return HTTPException(status_code=404, detail="User not found")
        return user

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 10) -> List[UserModel]:
        return await db.execute(select(self.model).where(self.model.user_status == 'active').offset(skip).limit(limit).order_by(self.model.id))
    
    async def create(self, db: AsyncSession, user_data):
        hashed_password = PasswordContext.get_password_hash(user_data.hashed_password)
        user = UserModel(
            user_email= user_data.user_email,
            user_firstname=user_data.user_firstname,
            hashed_password=hashed_password,
            user_status='active'
        )
        print(user)
        db.add(user)
        await db.commit()
        logger.info(f"User {user_data.user_firstname} created successfully")

    async def update(self, db: AsyncSession, id, user_data: UserSignIn):
        user = await db.get(UserModel, id)
        if not user or user.user_status == 'inactive':
            logger.error("User not found")
            return HTTPException(status_code=404, detail="User not found")
        user_data_dict = user_data.model_dump(exclude_unset=True, exclude=['user_email'])
        await db.execute(update(UserModel).where(UserModel.id == user.id).values(**user_data_dict))
        await db.commit()
        logger.info(f"User {id} updated successfully")
        return await db.get(UserModel, id)

    async def delete(self, db: AsyncSession, id):
        user = await db.get(UserModel, id)
        if not user or user.user_status == 'inactive':
            logger.error("User not found")
            return HTTPException(status_code=404, detail="User not found")
        await db.execute(update(UserModel).where(UserModel.id == user.id).values({'user_status': 'inactive'}))
        await db.commit()
        logger.info(f"User {id} is now inactive.")
        return {"message": f"User {id} is now inactive."}

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
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)

@user_endpoints.post("/user/")
async def create_user(user_data: UserSignIn, db: AsyncSession = Depends(get_db)):
    try:
        await crud.create(db=db, user_data=user_data)
        return {"result": f"User {user_data.user_firstname} created successfully"}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)

@user_endpoints.put("/user/{id}", response_model=Union[UserUpdate, ErrorResponse])
async def update_user(id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.update(db, id, user_data)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)

@user_endpoints.patch("/user/{id}")
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.delete(db, id)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500)
