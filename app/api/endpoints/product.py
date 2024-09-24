from fastapi import APIRouter

from app.crud.product import product_crud
from app.schemas.product import ProductCreate, ProductDB, ProductUpdate
from app.api import SessionDependency
from app.models import Product

router = APIRouter()


@router.post(
    "/",
    response_model=ProductDB
)
async def create_product(
        product: ProductCreate,
        session: SessionDependency
) -> Product:
    return await product_crud.create(
        obj_in=product, session=session
    )


@router.get("/", response_model=list[ProductDB])
async def products_list(
        session: SessionDependency
) -> list[Product]:
    return await product_crud.get_list(session=session)


@router.get(
    "/{product_id}",
    response_model=ProductDB
)
async def product_detail(product_id: int,
                         session: SessionDependency) -> Product:
    return await product_crud.get_or_404(obj_id=product_id, session=session)


@router.put(
    "/{product_id}",
    response_model=ProductDB
)
async def update_product(
        product_id: int,
        obj_in: ProductUpdate,
        session: SessionDependency
) -> Product:
    product = await product_crud.get_or_404(obj_id=product_id, session=session)
    return await product_crud.update(product, obj_in, session)


@router.delete("/{product_id}", response_model=ProductDB)
async def delete_product(product_id: int, session: SessionDependency):
    product = await product_crud.get_or_404(obj_id=product_id, session=session)
    return await product_crud.delete(product, session)
