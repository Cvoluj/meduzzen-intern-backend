import logging
import jwt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from typing import List, Optional

from app.models.models import UserModel
from app.schemas.user_schemas import UserSignIn, UserStatusEnum
from app.services.hashing import PasswordContext
from app.services.crud_base import CRUDBaseGet
from app.utils.auth0 import VerifyToken


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UserCRUD(CRUDBaseGet):

    def check_user(self, user: UserModel):
        if not user or user.user_status == UserStatusEnum.inactive:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[UserModel]:
        return await db.execute(select(self.model).where(self.model.user_email == email))

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 10) -> List[UserModel]:
        return await db.execute(select(self.model).where(self.model.user_status == UserStatusEnum.active).offset(skip).limit(limit).order_by(self.model.id))
    
    # async def get_user_by_token(self, db: AsyncSession, token: str):
        


    async def create(self, db: AsyncSession, user_data):
        hashed_password = PasswordContext.get_password_hash(user_data.hashed_password)
        user = UserModel(
            user_email= user_data.user_email,
            user_firstname=user_data.user_firstname,
            hashed_password=hashed_password,
            user_status='active'
        )

        db.add(user)
        await db.commit()
        logger.info(f"User {user_data.user_firstname} created successfully")
        return {"result": f"User {user_data.user_firstname} created successfully"}

    async def update(self, db: AsyncSession, id, user_data: UserSignIn):
        user = await db.get(UserModel, id)
        self.check_user(user)
        user_data_dict = user_data.model_dump(exclude_unset=True, exclude=['user_email'])
        await db.execute(update(UserModel).where(UserModel.id == user.id).values(**user_data_dict))
        await db.commit()
        logger.info(f"User {id} updated successfully")
        return await db.get(UserModel, id)
    
    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[UserModel]:
        user = await self.get_by_email(db=db, email=email)
        user = user.scalar()
        print(user)
        self.check_user(user)
        if not PasswordContext.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=404, detail="Password didn`t match")
        logger.info(f"User {user.user_firstname} authenticated successfully")
        return user

    async def delete(self, db: AsyncSession, id):
        user = await db.get(UserModel, id)
        self.check_user(user)
        await db.execute(update(UserModel).where(UserModel.id == user.id).values({'user_status': UserStatusEnum.inactive}))
        await db.commit()
        logger.info(f"User {id} is now inactive.")
        return {"message": f"User {id} is now inactive."}
