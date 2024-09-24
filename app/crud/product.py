from app.crud.base import CRUDBase
from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    pass


product_crud = CRUDProduct(Product)
