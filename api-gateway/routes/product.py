from fastapi import APIRouter
from methods.product import get_products_grpc
from models.product import ProductResponse

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
async def get_products():
    return await get_products_grpc()
