from fastapi import APIRouter


router = APIRouter()


@router.post("/")
async def create_product():
    pass


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