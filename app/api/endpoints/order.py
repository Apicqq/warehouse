from fastapi import APIRouter

from app.api import SessionDependency
from app.crud.order import order_crud
from app.schemas.order import OrderCreate, OrderUpdate, OrderDB, OrderBase

router = APIRouter()


@router.post(
    "/",
    response_model=OrderDB
)
async def create_order(
        order: OrderCreate,
        session: SessionDependency
):
    return await order_crud.create_order(obj_in=order, session=session)


@router.get("/", response_model=list[OrderDB])
async def orders_list(session: SessionDependency):
    return await order_crud.get_list(session=session)


@router.get("/{order_id}",
            response_model=OrderDB)
async def order_detail(order_id: int, session: SessionDependency):
    return await order_crud.get_order_by_id(order_id=order_id, session=session)


@router.patch("/{order_id}/status")
async def update_order_status(order_id: int):
    pass
