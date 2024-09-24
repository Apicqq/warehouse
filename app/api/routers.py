from fastapi import APIRouter

from app.api.endpoints import order_router, product_router


main_router = APIRouter()

main_router.include_router(order_router, prefix="/order", tags=["order"])
main_router.include_router(product_router, prefix="/product", tags=["product"])
