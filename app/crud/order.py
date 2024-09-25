from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate, \
    OrderDB


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):

    async def create_order(
            self,
            obj_in: OrderCreate,
            session: AsyncSession
    ):
        try:
            order_items = obj_in.order_items
            obj_in.order_items = []
            db_order = await self.create(
                obj_in=obj_in,
                session=session
            )
            order_id = db_order.id
            for order_item in order_items:
                session.add(
                    OrderItem(**order_item.model_dump(), order_id=order_id)
                )
            await session.commit()
            db_order = await self.get_order_by_id(
                order_id=order_id, session=session
            )
            return OrderDB.model_validate(db_order)
        except Exception:
            await session.rollback()
            return HTTPException(status_code=422, detail="Can't create order")

    async def _manage_product_stock(self, session, order_items, order_id):
        seen_products = {} # handle cases where the same product is being passed multiple times
        for order_item in order_items:
            product_pieces_to_remove = 0
            if order_item.product_id in seen_products:
                pass


    async def get_order_by_id(self, order_id: int, session: AsyncSession):
        obj = await session.execute(
            select(Order).where(Order.id == order_id).options(
                selectinload(Order.order_items)
            )
        )
        return obj.scalars().first()


class CRUDOrderItem(CRUDBase[OrderItem, OrderItemCreate, OrderItemCreate]):

    async def create_order_item(
            self,
            obj_in: OrderItemCreate,
            session: AsyncSession
    ):
        return await self.create(obj_in, session)


order_crud = CRUDOrder(Order)
