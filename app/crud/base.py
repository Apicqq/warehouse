from http import HTTPStatus
from typing import Generic, TypeVar, Optional, Sequence

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
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

    async def get_or_404(
            self, obj_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        """
        Получить объект по его ID либо вернуть ошибку 404, если такой объект
        не существует.
        """
        obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        db_obj = obj.scalars().first()
        if db_obj is not None:
            return db_obj
        else:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"{self.model.__name__} not found"
            )

    async def get_list(self, session: AsyncSession) -> Sequence[ModelType]:
        """
        Вернуть список всех объектов указанной модели.
        """
        objs = await session.execute(select(self.model))
        return objs.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession
    ) -> ModelType:
        """
        Создать новый объект указанной модели.
        """
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        return await self.push_to_db(db_obj, session)

    async def update(
            self,
            db_obj: ModelType,
            obj_in: UpdateSchemaType,
            session: AsyncSession,
    ) -> ModelType:
        """
        Обновить объект указанной модели.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        return await self.push_to_db(db_obj, session)

    async def delete(self, db_obj: ModelType, session: AsyncSession):
        """
        Удалить объект указанной модели.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def push_to_db(self, obj: Base, session: AsyncSession):
        """
        Поместить объект в базу данных.
        """
        await session.commit()
        await session.refresh(obj)
        return obj
