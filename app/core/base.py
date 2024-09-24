"""Импорты класса Base и всех моделей для Alembic."""

from app.core.db import Base  # noqa
from app.models.order import Order, OrderItem  # noqa
from app.models.product import Product # noqa

