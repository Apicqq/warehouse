from http import HTTPStatus

from fastapi import APIRouter

from app.api import SessionDependency
from app.crud.order import order_crud
from app.models.order import OrderStatus
from app.schemas.order import OrderCreate, OrderDB, Message

router = APIRouter()


@router.post(
    "/",
    response_model=OrderDB,
    responses={HTTPStatus.BAD_REQUEST: {"model": Message}}
)
async def create_order(
        order: OrderCreate,
        session: SessionDependency
) -> OrderDB:
    """
    Создать новый заказ.
    """
    return await order_crud.create_order(obj_in=order, session=session)


@router.get("/", response_model=list[OrderDB])
async def orders_list(session: SessionDependency) -> list[OrderDB]:
    """
    Вывести список всех заказов.
    """
    return await order_crud.get_orders_list(session=session)


@router.get(
    "/{order_id}",
    response_model=OrderDB,
    responses={HTTPStatus.NOT_FOUND: {"model": Message}}
)
async def order_detail(order_id: int, session: SessionDependency) -> OrderDB:
    """
    Вывести информацию о конкретном заказе.
    """
    return await order_crud.get_order_by_id_or_404(
        order_id=order_id, session=session
    )


@router.patch(
    "/{order_id}/status",
    response_model=OrderDB,
    responses={
        HTTPStatus.NOT_FOUND: {"model": Message},
    }
)
async def update_order_status(
        order_id: int,
        status: OrderStatus,
        session: SessionDependency,
) -> OrderDB:
    """
    Изменить статус заказа.
    """
    return await order_crud.change_order_status(
        order_id=order_id,
        status=status,
        session=session
    )
