from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Product(Base):
    __table_args__ = (
        CheckConstraint("price > 0", name="positive_price"),
        CheckConstraint(
            "amount_available >= 0", name="non-negative_amount_available"
        ),
    )

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    amount_available: Mapped[int] = mapped_column(Integer)

    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return (
            f"Product(id={self.id},"
            f" name={self.name},"
            f" description={self.description},"
            f" price={self.price},"
            f" amount_available={self.amount_available})"
            f" order_items={self.order_items}"
        )
