from collections.abc import Sequence
from typing import Generic, TypeVar, Optional, List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(
            self, obj_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return obj.scalars().first()

    async def get_list(self, session: AsyncSession) -> Sequence[ModelType]:
        objs = await session.execute(select(self.model))
        return objs.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession
    ) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
   