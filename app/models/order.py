from datetime import datetime
from enum import StrEnum, auto

from sqlalchemy import Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class OrderStatus(StrEnum):
    in_process = auto()
    sent = auto()
    delivered = auto()


class Order(Base):
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.in_process)
    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return (
            f"Order(id={self.id},"
            f" created_at={self.created_at},"
            f" status={self.status})"
        )


class OrderItem(Base):
    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="positive_quantity"
        ),
    )
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return (
            f"OrderItem(id={self.id},"
            f" order_id={self.order_id},"
            f" product_id={self.product_id},"
            f" quantity={self.quantity})"
        )
