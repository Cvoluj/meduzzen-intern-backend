from typing import TypeVar, Type, Optional, List, Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, alias

from app.models.models import Base

ModelType = TypeVar("ModelType", bound=Base)

class CRUDBaseGet():
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        return await db.get(self.model, id)

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 10
    ) -> List[ModelType]:
        return await db.execute(select(self.model).offset(skip).limit(limit))
        