from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveInt

from app.models.order import OrderStatus

class OrderItemBase(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt


class OrderItemDB(OrderItemBase):
    id: int
    order_id: PositiveInt
    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(OrderItemBase):
    pass

class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.in_process
    order_items: list[OrderItemBase]

class OrderCreate(OrderBase):
    order_items: list[OrderItemCreate]

class OrderUpdate(OrderBase):
    pass

class OrderDB(OrderBase):
    id: int
    created_at: datetime
    status: OrderStatus
    order_items: list[OrderItemDB]
    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    message: str

class OrderChangeStatus(BaseModel):
    status: OrderStatus
