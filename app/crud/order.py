from http import HTTPStatus
from typing import Optional, Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.product import Product
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderItemCreate,
    OrderDB,
)


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):

    async def create_order(
        self, obj_in: OrderCreate, session: AsyncSession
    ) -> OrderDB:
        """
        Создать новый заказ.

        Метод учитывает информацию о продуктах в заказе, проверяет доступный
        остаток и в случае, если для указанного продукта требуемый остаток
        меньше, чем есть в наличии,
        вызывает исключение HTTPException со статусом 400.
        """
        order_items = obj_in.order_items
        obj_in.order_items = []
        db_order = Order(**obj_in.model_dump(exclude={"order_items"}))
        session.add(db_order)
        await session.flush()
        order_id = db_order.id
        await self._manage_product_stock(session, order_items)
        for order_item in order_items:
            session.add(
                OrderItem(**order_item.model_dump(), order_id=order_id)
            )
        await session.commit()
        db_order = await self.get_order_by_id_or_404(
            order_id=order_id, session=session
        )
        return OrderDB.model_validate(db_order)

    async def _manage_product_stock(
        self, session: AsyncSession, order_items: list[OrderItemCreate]
    ) -> None:
        """
        Вспомогательный метод для метода создания заказа, который проверяет
        остаток каждого товара в заказе, и если остаток меньше, чем требуется,
        то вызывается исключение HTTPException с кодом 400.

        Метод также учитывает случаи, когда один и тот же продукт добавлен
        в заказ несколько раз.
        """
        seen_products = {}  # для случаев, когда один и тот же продукт
        # передаётся в заказ несколько раз
        for order_item in order_items:
            product_id = order_item.product_id
            quantity = order_item.quantity
            if product_id in seen_products:
                seen_products[product_id] += quantity
            else:
                seen_products[product_id] = quantity

        for product_id, quantity in seen_products.items():
            product = await session.execute(
                select(Product).where(Product.id == product_id)
            )
            product = product.scalars().first()
            if product.amount_available < quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Не удалось создать заказ:"
                    f" на складе недостаточно товара {product.name}",
                )
            product.amount_available -= quantity
            session.add(product)
        await session.commit()

    async def get_order_by_id_or_404(
        self, order_id: int, session: AsyncSession
    ) -> Optional[Order]:
        """
        Вернуть объект заказа по его ID либо вернуть ошибку 404, если такой
        объект не существует.
        """
        obj = await session.execute(
            select(self.model)
            .where(self.model.id == order_id)
            .options(selectinload(Order.order_items))
        )
        db_obj = obj.scalars().first()
        if db_obj is not None:
            return db_obj
        else:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )

    async def get_orders_list(self, session: AsyncSession) -> Sequence[Order]:
        """
        Вернуть список всех заказов.
        """
        objs = await session.execute(
            select(self.model).options(selectinload(Order.order_items))
        )
        return objs.scalars().all()

    async def change_order_status(
        self, order_id: int, status: OrderStatus, session: AsyncSession
    ) -> Optional[Order]:
        """
        Изменить статус заказа.
        """
        obj = await self.get_order_by_id_or_404(
            order_id=order_id, session=session
        )
        obj.status = status
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj


order_crud = CRUDOrder(Order)
