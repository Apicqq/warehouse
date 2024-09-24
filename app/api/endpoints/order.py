from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def create_order():
    pass


@router.get("/")
async def orders_list():
    pass


@router.get("/{order_id}")
async def order_detail(order_id: int):
    pass


@router.patch("/{order_id}/status")
async def update_order_status(order_id: int):
    pass
