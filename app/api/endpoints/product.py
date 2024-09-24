from fastapi import APIRouter

from app.crud.product import product_crud
from app.api import SessionDependency
from app.models import Product

router = APIRouter()


@router.post("/")
async def create_product(
        product,
        session: SessionDependency
) -> Product:
    return await product_crud.create(
        obj_in=product, session=session
    )


@router.get("/")
async def products_list():
    pass


@router.get("/{product_id}")
async def product_detail(product_id: int):
    pass


@router.patch("/{product_id}")
async def update_product(product_id: int):
    pass


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    pass