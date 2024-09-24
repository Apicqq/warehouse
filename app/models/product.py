from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class Product(Base):
    __table_args__ = (
        CheckConstraint("price > 0", name="positive_price"),
    )

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    amount_available: Mapped[int] = mapped_column(Integer)

    order_items = relationship("OrderItem", back_populates="product")