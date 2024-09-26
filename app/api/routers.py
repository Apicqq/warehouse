from fastapi import APIRouter

from app.api.endpoints import order_router, product_router


main_router = APIRouter()

main_router.include_router(order_router, prefix="/orders", tags=["order"])
main_router.include_router(
    product_router, prefix="/products", tags=["product"]
)
