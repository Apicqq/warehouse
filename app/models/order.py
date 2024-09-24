from datetime import datetime
from enum import StrEnum, auto

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

class OrderStatus(StrEnum):
    in_process = auto()
    sent = auto()
    delivered = auto()

class Order(Base):
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.in_process)
    order_items = relationship("OrderItem", back_populates="order")



class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")